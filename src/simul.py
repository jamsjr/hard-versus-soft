#!/usr/bin/env python
# coding: utf-8

from SimPy.Simulation import *
from SimPy.SimPlot import *
from random import expovariate
import os
import math

server_no = 0

def tn(a):
  return type(a).__name__

def mean(l):
  return sum(l)/float(len(l))

class PeriodicTask(Process):
  def start_running(self,sched,c,t,d):
    last_request = 0
    while True:
      next_request = last_request + t
      last_request = next_request
      next_deadline = next_request + d
      yield hold,self,next_request-now()
      arrive = now()
      yield (request,self,sched,-next_deadline),(hold,self,d-c)
      if self.acquired(sched):
        ac = now()
        yield hold,self,c
        yield release,self,sched
      else:
        pass
        #print "Lost deadline"

class HardCBS(Process):
  """Um CBS aqui está implementado como um processo normal.
Em vez dos processos se agendarem, se executarem, ele faz isso,
mantento o bookkeeping que precisar.
Eu ignoro prioridades dentro desse cbs.
"""
  
  def __init__(self, *args, **kwargs):
    if "lose_deadlines" in kwargs:
      self.lose_deadlines = kwargs.pop("lose_deadlines")
    else:
      self.lose_deadlines = False
    super(HardCBS, self).__init__(*args, **kwargs)

  def initialize(self,scheduler,task,server_util=None):
    global server_no
    server_period = mean([x[2]-x[0] for x in task])
    self.name = tn(self)+str(server_no)
    server_no += 1
    if not server_util:
      server_util = mean([x[1]/(x[2] - x[0]) for x in task[:-1]])
    server_capacity = server_util*server_period
    response_time = Monitor(self.name+" Response time")
    lost_deadlines = Monitor("Lost deadlines "+self.name)
    lateness = Monitor(self.name + " Lateness")
    delay_time = Monitor(self.name+ " Delay")
    resp_interva = Monitor(self.name + " Response Interval")
    self.monitors = {"response_time": response_time,
                     "lost_deadlines": lost_deadlines,
                     "lateness": lateness,
                     "delay_time": delay_time,
                     "resp_int": resp_interva}
    print self.name, "capacity", server_capacity, "period", server_period
    process = self.start_running(scheduler, task, server_capacity, server_period)
    activate(self, process, at=0.)

  def wait_until_next_deadline(self, this_deadline, period):
    if this_deadline > now():
      return hold, self, this_deadline-now()
    return hold, self, 0

  def arrive_reschedule(self, cap, period, this_deadline, curr_cap, cost):
    util = float(cap)/period
    if now() + (curr_cap/cap)*period >= this_deadline:
      return cap, now()+period
    else:
      return curr_cap, this_deadline

  def check_deadline(self, time, deadline):
    if time > deadline and self.lose_deadlines:
      self.monitors['lost_deadlines'].observe(time)
      return True
    return False
  
  def finish(self, time, started, deadline, cost, last_finished):
    self.monitors['resp_int'].observe(time - last_finished)
    self.monitors['response_time'].observe(time - started)
    if not self.lose_deadlines:
      self.monitors['lateness'].observe(time - deadline)

  def start_running(self, sched, tasks, cap, period):
    last_finished = now()
    curr_cap = cap
    dk = period
    self.i = 0
    for (started, cost, deadline) in tasks:
      self.i += 1
      if now() <= started: yield hold,self,started-now()
      if now() >= dk:
        dk = now() + period
        curr_cap = cap
      else:
        curr_cap, dk = self.arrive_reschedule(cap, period, dk, curr_cap, cost)
      while True:
        if self.check_deadline(now(), deadline): break
        if self.lose_deadlines:
          yield (request,self,sched,-dk),(hold,self,deadline-now()) 
          if (not self.acquired(sched) or 
                self.check_deadline(now(), deadline)): 
              break
        else:
          yield (request,self,sched,-dk)
        this_run = min(curr_cap, cost)
        self.monitors['delay_time'].observe(now() - started)
        yield hold, self, this_run
        yield release, self, sched
        cost -= this_run
        curr_cap -= this_run
        if self.check_deadline(now(), deadline): break
        if cost <= 0:
          self.finish(now(), started, deadline, cost, last_finished)
          last_finished = now()
          break
        if curr_cap <= 0:
          yield self.wait_until_next_deadline(dk, period)
          curr_cap = cap
          dk += period

class SoftCBS(HardCBS):
  def wait_until_next_deadline(self, this_deadline, period):
    return hold, self, 0


def load_data_file(name):
  points =  [map(float, line.split()) for line in file(name)]
  intervals = [x[0] for x in points[1:]] + [1000]
  return [points[i]+[intervals[i]] for i in xrange(len(points))]

def make_normal_tasks(mean_cost, var_cost, period, n):
  start = 0
  tasks = []
  for i in xrange(n):
    dead = start+period
    cost = random.gauss(mean_cost, var_cost)
    tasks.append((start, cost, dead))
    start = dead
  return tasks

def concatenate_tasks(t1, t2):
  dmax = t1[-1][2]
  return t1 + [(a+dmax,c,d+dmax) for a,c,d in t2]

def run():
  soft_tasks = load_data_file("/home/top/programas/test/data/decode-trace-eve.txt")
  
  scheduler = Resource(name='edf',preemptable=1,monitored=True,qType=PriorityQ)
  
  initialize()
  
  servs = []
  
  for server in [SoftCBS]:
    t0 = make_normal_tasks(0.4, 0.01, 1, 3000)
    t1 = make_normal_tasks(0.6, 0.01, 1, 3000)
    t2 = make_normal_tasks(0.4, 0.01, 1, 3000)
    s = server(lose_deadlines=True)
    t = concatenate_tasks(concatenate_tasks(t0,t1),t2)
    s.initialize(scheduler, t, server_util=0.5)
    servs.append(s)
  
  p = PeriodicTask()
  activate(p, p.start_running(scheduler, 2.5, 5, 5), at=0.)
  
  print simulate(9000)
  plt = SimPlot()
  
  for s in servs:
    monitors = s.monitors
    Mon = monitors['response_time']
    dead = monitors['lost_deadlines']
    print Mon.name, "lost %2.2f%%" % (100.*len(dead)/(len(Mon)+len(dead))),
    print "of the deadlines"
    for mon in 'response_time', 'resp_int', 'lateness', 'delay_time':
      Mon = monitors[mon]
      if len(Mon):
        print Mon.name, Mon.mean(), "stddev", math.sqrt(Mon.var())
    for m in 'response_time', 'resp_int', 'lateness', 'delay_time':
      m = monitors[m]
      if len(m):
        print m.name
        plt.plotLine(m,yaxis='automatic',xlab="Monitor "+m.name)
    for h in 'response_time', 'resp_int', 'lateness', 'delay_time':
      h = monitors[h]
      if len(h):
        print h.name
        Histo = h.histogram(low=0.,high=max(a[1] for a in h),nbins=400)
        plt.plotHistogram(Histo, xlab='Time', title=h.name+" histogram",width=2)
  plt.mainloop()

print "Loaded"

if __name__ == '__main__':
  run()
