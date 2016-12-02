#! /usr/bin/python
# work out the mass of investment casting and water needed

import math

# all dimensions in mm
# all masses in g

mm_per_in = 25.4
mm3_per_in3 = math.pow(25.4, 3.0)
mm3_per_cm3 = math.pow(10.0, 3.0)

g_per_lb = 453.592
g_per_oz = 28.3495

# an extra 5% of material
extra_factor = 1.05

# from the kerr satin 20 docs: 20 in3 needs = 1 lb of investment
investment_density = g_per_lb / (20.0 * mm3_per_in3) # g per mm3

# heavy castings: 38 ml of water to 100g of powder
heavy_water_ratio = 38.0 / 100.0 # ml per g

# light castings: 40 ml of water to 100g of powder
light_water_ratio = 40.0 / 100.0 # ml per g

def flask_vol(d, h):
  r = d / 2.0
  return  math.pi * math.pow(r, 2.0) * h

def main():

  pattern_vol = 167.0 * mm3_per_cm3
  vol = flask_vol(2.5 * mm_per_in, 9.0 * mm_per_in)
  vol -= pattern_vol
  vol *= extra_factor

  investment = vol * investment_density
  water = investment * heavy_water_ratio

  print('investment: %.1f g' % investment)
  #print('investment: %.1f oz' % (investment/ g_per_oz))
  #print('investment: %.1f lb' % (investment/ g_per_lb))
  print('water: %.1f ml' % water)

main()
