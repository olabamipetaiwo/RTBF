# verify

_Run at 2026-09-23T10:22:16_

```text

==================================================================
LESS SENSITIVE — EXPECTATION by method (Q4.4)
==================================================================
               option   test  p_raw  p_holm  cramers_v sig
  permanently deleted   chi2 0.7261     1.0      0.090    
       made invisible fisher 0.1459     1.0      0.186    
     not ref. current   chi2 0.4372     1.0      0.130    
      not ref. future   chi2 0.9893     1.0      0.027    
not used for training fisher 0.2474     1.0      0.163    
             not sure fisher 0.4339     1.0      0.153    
                other fisher 0.4783     1.0      0.156    

==================================================================
LESS SENSITIVE — VERIFICATION by method (Q4.5)
==================================================================
                option   test  p_raw  p_holm  cramers_v sig
      asked same convo fisher 0.0002  0.0014      0.351   *
       asked new convo fisher 0.0010  0.0068      0.314   *
      checked settings fisher 0.0769  0.3846      0.219    
            checked UI fisher 0.6118  1.0000      0.109    
privacy-portal request fisher 0.6552  1.0000      0.100    
      did NOT know how   chi2 0.0011  0.0068      0.315   *
       did NOT want to fisher 0.4957  1.0000      0.124    
                 other fisher 0.3511  1.0000      0.142    

==================================================================
MORE SENSITIVE — EXPECTATION by method (Q5.4)
==================================================================
               option   test  p_raw  p_holm  cramers_v sig
  permanently deleted   chi2 0.6338  1.0000      0.105    
       made invisible fisher 0.1231  0.6155      0.185    
     not ref. current   chi2 0.0079  0.0550      0.276    
      not ref. future   chi2 0.0276  0.1653      0.242    
not used for training fisher 0.3924  1.0000      0.138    
             not sure fisher 1.0000  1.0000      0.050    
                other fisher 0.4872  1.0000      0.137    

==================================================================
MORE SENSITIVE — VERIFICATION by method (Q5.5)
==================================================================
                option   test  p_raw  p_holm  cramers_v sig
      asked same convo fisher 0.0048  0.0385      0.314   *
       asked new convo fisher 0.2774  0.9884      0.161    
      checked settings fisher 0.0065  0.0458      0.296   *
            checked UI fisher 0.2188  0.9884      0.173    
privacy-portal request fisher 0.1977  0.9884      0.186    
      did NOT know how   chi2 0.0364  0.2184      0.234    
       did NOT want to fisher 0.8950  1.0000      0.051    
                 other fisher 0.5505  1.0000      0.113    
```
