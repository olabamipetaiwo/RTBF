# verify

_Run at 2026-08-07T14:19:21_

```text

==================================================================
LESS SENSITIVE — EXPECTATION by method (Q4.4)
==================================================================
               option   test  p_raw  p_holm  cramers_v sig
  permanently deleted   chi2 0.7261     1.0      0.090    
       made invisible fisher 0.1491     1.0      0.186    
     not ref. current   chi2 0.4372     1.0      0.130    
      not ref. future   chi2 0.9893     1.0      0.027    
not used for training fisher 0.2454     1.0      0.163    
             not sure fisher 0.4235     1.0      0.153    
                other fisher 0.4790     1.0      0.156    

==================================================================
LESS SENSITIVE — VERIFICATION by method (Q4.5)
==================================================================
                option   test  p_raw  p_holm  cramers_v sig
      asked same convo fisher 0.0004  0.0032      0.351   *
       asked new convo fisher 0.0010  0.0070      0.314   *
      checked settings fisher 0.0784  0.3920      0.219    
            checked UI fisher 0.6072  1.0000      0.109    
privacy-portal request fisher 0.6567  1.0000      0.100    
      did NOT know how   chi2 0.0011  0.0070      0.315   *
       did NOT want to fisher 0.4861  1.0000      0.124    
                 other fisher 0.3546  1.0000      0.142    

==================================================================
MORE SENSITIVE — EXPECTATION by method (Q5.4)
==================================================================
               option   test  p_raw  p_holm  cramers_v sig
  permanently deleted   chi2 0.6299  1.0000      0.105    
       made invisible fisher 0.1275  0.6375      0.183    
     not ref. current   chi2 0.0077  0.0540      0.275    
      not ref. future   chi2 0.0295  0.1772      0.239    
not used for training fisher 0.3987  1.0000      0.135    
             not sure fisher 1.0000  1.0000      0.050    
                other fisher 0.4893  1.0000      0.137    

==================================================================
MORE SENSITIVE — VERIFICATION by method (Q5.5)
==================================================================
                option   test  p_raw  p_holm  cramers_v sig
      asked same convo fisher 0.0044  0.0352      0.315   *
       asked new convo fisher 0.2629  0.9920      0.163    
      checked settings fisher 0.0057  0.0399      0.297   *
            checked UI fisher 0.2103  0.9920      0.175    
privacy-portal request fisher 0.1984  0.9920      0.186    
      did NOT know how   chi2 0.0437  0.2625      0.227    
       did NOT want to fisher 0.8937  1.0000      0.053    
                 other fisher 0.6643  1.0000      0.113    
```
