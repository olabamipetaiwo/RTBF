# verify

_Run at 2026-08-07T14:24:09_

```text

==================================================================
LESS SENSITIVE — EXPECTATION by method (Q4.4)
==================================================================
               option   test  p_raw  p_holm  cramers_v sig
  permanently deleted   chi2 0.7261     1.0      0.090    
       made invisible fisher 0.1442     1.0      0.186    
     not ref. current   chi2 0.4372     1.0      0.130    
      not ref. future   chi2 0.9893     1.0      0.027    
not used for training fisher 0.2409     1.0      0.163    
             not sure fisher 0.4366     1.0      0.153    
                other fisher 0.4837     1.0      0.156    

==================================================================
LESS SENSITIVE — VERIFICATION by method (Q4.5)
==================================================================
                option   test  p_raw  p_holm  cramers_v sig
      asked same convo fisher 0.0002  0.0016      0.351   *
       asked new convo fisher 0.0017  0.0102      0.314   *
      checked settings fisher 0.0740  0.3700      0.219    
            checked UI fisher 0.6184  1.0000      0.109    
privacy-portal request fisher 0.6568  1.0000      0.100    
      did NOT know how   chi2 0.0011  0.0080      0.315   *
       did NOT want to fisher 0.4940  1.0000      0.124    
                 other fisher 0.3562  1.0000      0.142    

==================================================================
MORE SENSITIVE — EXPECTATION by method (Q5.4)
==================================================================
               option   test  p_raw  p_holm  cramers_v sig
  permanently deleted   chi2 0.6299  1.0000      0.105    
       made invisible fisher 0.1282  0.6410      0.183    
     not ref. current   chi2 0.0077  0.0540      0.275    
      not ref. future   chi2 0.0295  0.1772      0.239    
not used for training fisher 0.3950  1.0000      0.135    
             not sure fisher 1.0000  1.0000      0.050    
                other fisher 0.4697  1.0000      0.137    

==================================================================
MORE SENSITIVE — VERIFICATION by method (Q5.5)
==================================================================
                option   test  p_raw  p_holm  cramers_v sig
      asked same convo fisher 0.0046  0.0368      0.315   *
       asked new convo fisher 0.2605  0.9425      0.163    
      checked settings fisher 0.0063  0.0441      0.297   *
            checked UI fisher 0.2130  0.9425      0.175    
privacy-portal request fisher 0.1885  0.9425      0.186    
      did NOT know how   chi2 0.0437  0.2625      0.227    
       did NOT want to fisher 0.8929  1.0000      0.053    
                 other fisher 0.6592  1.0000      0.113    
```
