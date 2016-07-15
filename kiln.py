#! /usr/bin/python
# work out total times for klin temperature ramp/hold profiles

# temperatures are stored in celsius units
# times are stored in minute units

import math

def f2c(f):
  return 100.0 * ((f - 32.0) / 180.0)

def c2f(c):
  return (180.0 * (c / 100.0)) + 32.0

def f2c_rate(f):
  return (100.0/180.0) * f

def c2f_rate(c):
  return (180.0/100.0) * c

_room_temp = f2c(70)
_hour = 60

def time_str(t):
  """return a time in hours and minutes"""
  h = math.floor(t / _hour)
  m = int(t - (_hour * h))
  s = []
  if h != 0:
    s.append('%dh' % h)
  if m != 0:
    s.append('%dm' % m)
  if h == 0 and m == 0:
    s.append('0m')
  return ''.join(s)

class segment:

  def __init__(self, name, target, rate, hold):
    self.name = name
    self.target = target
    self.rate = rate
    self.hold = hold

  def ramp(self, t):
    if t == self.target:
      # no temperature change
      ramp_time = 0.0
    elif t < self.target:
      # heating up
      ramp_time = (self.target - t)/self.rate
    else:
      # cooling down
      ramp_time = (t - self.target)/self.rate
    s = []
    s.append('%-22s' % self.name)
    s.append('%.1f > %.1f' % (c2f(t), c2f(self.target)))
    s.append('rate %.1f' % (c2f_rate(self.rate) * 60))
    s.append('ramp_time %s' % time_str(ramp_time))
    s.append('hold_time %s' % time_str(self.hold))
    return (ramp_time + self.hold, self.target, ' '.join(s))

class profile:

  def __init__(self, name, temp):
    self.name = name
    self.segments = []
    self.temp = temp

  def add(self, s):
    self.segments.append(s)

  def __str__(self):
    s = []
    s.append(self.name)
    total_time = 0
    temp = self.temp
    for seg in self.segments:
      (time, end_temp, description) = seg.ramp(temp)
      s.append(description)
      temp = end_temp
      total_time += time
    s.append('total time %s' % time_str(total_time))
    return '\n'.join(s)

def main():

  rate = f2c_rate(540.0/60.0)
  p = profile('8hr wax burnout', _room_temp)
  p.add(segment('water elimination', f2c(300), rate, 1 * _hour))
  p.add(segment('wax elimination', f2c(700), rate, 2 * _hour))
  p.add(segment('thermal expansion', f2c(900), rate, 1 * _hour))
  p.add(segment('complete elimination', f2c(1350), rate, 3 * _hour))
  p.add(segment('casting temperature', f2c(1000), rate, 1 * _hour))
  print(p)

  rate = f2c_rate(200.0/60.0)
  p = profile('bisque firing', _room_temp)
  p.add(segment('1st water removal', f2c(200), rate, 2 * _hour))
  p.add(segment('2nd water removal', f2c(300), rate, 0.5 * _hour))
  p.add(segment('quartz inversion', f2c(1060), rate, 0.5 * _hour))
  p.add(segment('balancing', f2c(1832), rate, 0))
  print(p)

main()
