# platform_breakdown

_Run at 2026-10-27T02:58:21_

```text
Per-platform breakdown (see platforms/how.md, step 1).

===== chatgpt =====
-- MASTER --
outcomes:
  recall success  10
  recall failed   5
  can't tell      3
probe that retrieved the token (10 recall-success cells):
  found by R1, R2, R3                                          3
  found by R1, R3                                              3
  found by R1                                                  2
  found by R1, R2                                              2
  R3 involved in 6 of 10
same conversation (rows) against new-conversation outcome (columns), 2 typed-erasure cells:
  recoverability        recall success
  same_conversation_r1                
  FOUND                              2
main-grid cells:
  CH-I1-E6     Clear all chat history (bulk)  R1=FOUND R2=FOUND R3=NOT FOUND -> recall success
  CH-I2-E6     Clear all chat history (bulk)  R1=NOT FOUND R2=NOT FOUND R3=NOT FOUND -> recall failed
  CH-I3-E6     Clear all chat history (bulk)  R1=FOUND R2=NOT FOUND R3=FOUND -> recall success
  CH-I1-E4     Clear all memories             R1=FOUND R2=FOUND R3=FOUND -> recall success
  CH-I2-E4     Clear all memories             R1=NOT FOUND R2=NOT FOUND R3=NOT FOUND -> recall failed
  CH-I3-E4     Clear all memories             R1=FOUND R2=NOT FOUND R3=FOUND -> recall success
  CH-I1-E5     Clear custom instructions      R1=FOUND R2=FOUND R3=NOT FOUND -> recall success
  CH-I2-E5     Clear custom instructions      R1=FOUND R2=FOUND R3=FOUND -> recall success
  CH-I3-E5     Clear custom instructions      R1=NOT FOUND R2=NOT FOUND R3=NOT FOUND -> recall failed
  CH-I1-E2     Delete conversation            R1=NOT FOUND R2=NOT FOUND R3=NOT FOUND -> can't tell
  CH-I2-E2     Delete conversation            R1=NOT FOUND R2=NOT FOUND R3=NOT FOUND -> can't tell
  CH-I3-E2     Delete conversation            R1=FOUND R2=NOT FOUND R3=NOT FOUND -> recall success
  CH-I1-E7     MAXIMAL                        R1=NOT FOUND R2=NOT FOUND R3=NOT FOUND -> can't tell
  CH-I2-E7     MAXIMAL                        R1=NOT FOUND R2=nan R3=NOT FOUND -> recall failed
  CH-I3-E7     MAXIMAL                        R1=NOT FOUND R2=nan R3=NOT FOUND -> recall failed
  CH-I1-E1     NL forget prompt               R1=FOUND R2=NOT FOUND R3=NOT FOUND -> recall success
  CH-I2-E1     NL forget prompt               R1=FOUND R2=FOUND R3=FOUND -> recall success
  CH-I3-E1     NL forget prompt               R1=FOUND R2=NOT FOUND R3=FOUND -> recall success
original token retrieved after replacement: 2
  CH-I1-E2: original token 'Skinny Stopper' in the new-conversation recall replies
  CH-I2-E2: original token 'Nutcase Taps' in the new-conversation recall replies

-- NL FORGET --
outcomes:
  recall success  108
  recall failed   23
  not recalled    5
  can't tell      2
probe that retrieved the token (108 recall-success cells):
  found by R1                                                  94
  token surfaced in a sibling cell's recall (sibling rule)     13
  found by R2                                                  1
  R3 involved in 0 of 108
same conversation (rows) against new-conversation outcome (columns), 133 typed-erasure cells:
  recoverability        can't tell  recall failed  recall success
  same_conversation_r1                                           
  FOUND                          0              0               4
  NOT FOUND                      2             23             104

===== claude =====
-- MASTER --
outcomes:
  recall failed   10
  recall success  3
  can't tell      2
probe that retrieved the token (3 recall-success cells):
  found by R1, R3                                              3
  R3 involved in 3 of 3
same conversation (rows) against new-conversation outcome (columns), 2 typed-erasure cells:
  recoverability        can't tell  recall failed
  same_conversation_r1                           
  FOUND                          1              0
  NOT FOUND                      0              1
main-grid cells:
  CL-I1-E3     Clear all memories             R1=NOT FOUND R2=NOT FOUND R3=NOT FOUND -> can't tell
  CL-I2-E3     Clear all memories             R1=NOT FOUND R2=NOT FOUND R3=NOT FOUND -> recall failed
  CL-I3-E3     Clear all memories             R1=NOT FOUND R2=NOT FOUND R3=NOT FOUND -> recall failed
  CL-I1-E1     Delete conversation            R1=FOUND R2=NOT FOUND R3=FOUND -> recall success
  CL-I2-E1     Delete conversation            R1=FOUND R2=NOT FOUND R3=FOUND -> recall success
  CL-I3-E1     Delete conversation            R1=FOUND R2=NOT FOUND R3=FOUND -> recall success
  CL-I1-E2     Delete individual memory edit  R1=NOT FOUND R2=NOT FOUND R3=NOT FOUND -> recall failed
  CL-I2-E2     Delete individual memory edit  R1=NOT FOUND R2=NOT FOUND R3=NOT FOUND -> recall failed
  CL-I3-E2     Delete individual memory edit  R1=NOT FOUND R2=NOT FOUND R3=NOT FOUND -> recall failed
  CL-I1-E5     MAXIMAL                        R1=NOT FOUND R2=NOT FOUND R3=NOT FOUND -> recall failed
  CL-I2-E5     MAXIMAL                        R1=NOT FOUND R2=NOT FOUND R3=NOT FOUND -> recall failed
  CL-I3-E5     MAXIMAL                        R1=NOT FOUND R2=NOT FOUND R3=NOT FOUND -> recall failed
  CL-I1-E4     NL forget command              R1=NOT FOUND R2=NOT FOUND R3=NOT FOUND -> can't tell
  CL-I2-E4     NL forget command              R1=NOT FOUND R2=NOT FOUND R3=NOT FOUND -> recall failed
  CL-I3-E4     NL forget command              R1=NOT FOUND R2=NOT FOUND R3=NOT FOUND -> recall failed
original token retrieved after replacement: 0

-- NL FORGET --
outcomes:
  recall failed   131
  not recalled    5
  can't tell      2
probe that retrieved the token (0 recall-success cells):
  R3 involved in 0 of 0
same conversation (rows) against new-conversation outcome (columns), 132 typed-erasure cells:
  recoverability        can't tell  recall failed
  same_conversation_r1                           
  FOUND                          2             86
  NOT FOUND                      0             44

===== copilot =====
-- MASTER --
outcomes:
  recall success  5
  can't tell      3
  not recalled    2
  recall failed   2
probe that retrieved the token (5 recall-success cells):
  found by R1                                                  5
  R3 involved in 0 of 5
main-grid cells:
  CO-I1-E1     Conversation history deletion  R1=NOT FOUND R2=NOT FOUND R3=NOT FOUND -> can't tell
  CO-I2-E1     Conversation history deletion  R1=FOUND R2=NOT FOUND R3=NOT FOUND -> recall success
  CO-I1-E2     Delete all memory              R1=FOUND R2=NOT FOUND R3=NOT FOUND -> recall success
  CO-I2-E2     Delete all memory              R1=FOUND R2=NOT FOUND R3=NOT FOUND -> recall success
  CO-I1-E4     Granular facts editor          R1=NOT RECALLED R2=NOT RECALLED R3=NOT RECALLED -> not recalled
  CO-I2-E4     Granular facts editor          R1=FOUND R2=NOT FOUND R3=NOT FOUND -> recall success
  CO-I1-E6     MAXIMAL                        R1=NOT RECALLED R2=NOT RECALLED R3=NOT RECALLED -> not recalled
  CO-I2-E6     MAXIMAL                        R1=NOT FOUND R2=NOT FOUND R3=NOT FOUND -> recall failed
  CO-I1-E3     NL forget command              R1=NOT FOUND R2=NOT FOUND R3=NOT FOUND -> can't tell
  CO-I2-E3     NL forget command              R1=FOUND R2=NOT FOUND R3=NOT FOUND -> recall success
  CO-I1-E5     Privacy Dashboard              R1=NOT FOUND R2=nan R3=NOT FOUND -> can't tell
  CO-I2-E5     Privacy Dashboard              R1=NOT FOUND R2=nan R3=NOT FOUND -> recall failed
original token retrieved after replacement: 1
  CO-I2-E4: original token 'Length Default Waffle Negative' in the new-conversation recall replies

-- NL FORGET --
outcomes:
  not recalled    70
  can't tell      42
  recall failed   25
  pending review  1
probe that retrieved the token (0 recall-success cells):
  R3 involved in 0 of 0
same conversation (rows) against new-conversation outcome (columns), 15 typed-erasure cells:
  recoverability        can't tell  recall failed
  same_conversation_r1                           
  FOUND                          4              4
  NOT FOUND                      3              4

===== deepseek =====
-- MASTER --
outcomes:
  can't tell      4
probe that retrieved the token (0 recall-success cells):
  R3 involved in 0 of 0
same conversation (rows) against new-conversation outcome (columns), 1 typed-erasure cells:
  recoverability        can't tell
  same_conversation_r1            
  NOT FOUND                      1
main-grid cells:
  DE-I1-E2     Delete all history             R1=NOT FOUND R2=nan R3=NOT FOUND -> can't tell
  DE-I1-E1     Delete single conversation     R1=NOT FOUND R2=nan R3=NOT FOUND -> can't tell
  DE-I1-E4     MAXIMAL                        R1=NOT FOUND R2=nan R3=NOT FOUND -> can't tell
  DE-I1-E3     NL forget prompt               R1=NOT FOUND R2=nan R3=NOT FOUND -> can't tell
original token retrieved after replacement: 0

-- NL FORGET --
outcomes:
  can't tell      133
  not recalled    5
probe that retrieved the token (0 recall-success cells):
  R3 involved in 0 of 0
same conversation (rows) against new-conversation outcome (columns), 133 typed-erasure cells:
  recoverability        can't tell
  same_conversation_r1            
  FOUND                         90
  NOT FOUND                     43

===== gemini =====
-- MASTER --
outcomes:
  can't tell      5
  recall success  5
  recall failed   2
probe that retrieved the token (5 recall-success cells):
  found by R1, R3                                              2
  found by R1, R2, R3                                          2
  found by R1, R2                                              1
  R3 involved in 4 of 5
same conversation (rows) against new-conversation outcome (columns), 1 typed-erasure cells:
  recoverability        can't tell
  same_conversation_r1            
  NOT FOUND                      1
main-grid cells:
  GE-I1-E5     Delete all Saved info          R1=FOUND R2=NOT FOUND R3=FOUND -> can't tell
  GE-I2-E5     Delete all Saved info          R1=NOT FOUND R2=NOT FOUND R3=NOT FOUND -> recall failed
  GE-I1-E3     Delete all activity            R1=FOUND R2=NOT FOUND R3=FOUND -> recall success
  GE-I2-E3     Delete all activity            R1=FOUND R2=FOUND R3=NOT FOUND -> recall success
  GE-I1-E4     Delete single Saved info item  R1=FOUND R2=NOT FOUND R3=FOUND -> recall success
  GE-I2-E4     Delete single Saved info item  R1=FOUND R2=FOUND R3=FOUND -> can't tell
  GE-I1-E2     Delete single conversation     R1=NOT FOUND R2=NOT FOUND R3=NOT FOUND -> can't tell
  GE-I2-E2     Delete single conversation     R1=FOUND R2=FOUND R3=FOUND -> recall success
  GE-I1-E6     MAXIMAL                        R1=NOT FOUND R2=NOT FOUND R3=NOT FOUND -> can't tell
  GE-I2-E6     MAXIMAL                        R1=NOT FOUND R2=NOT FOUND R3=NOT FOUND -> recall failed
  GE-I1-E1     NL forget prompt               R1=NOT FOUND R2=NOT FOUND R3=NOT FOUND -> can't tell
  GE-I2-E1     NL forget prompt               R1=FOUND R2=FOUND R3=FOUND -> recall success
original token retrieved after replacement: 0

-- NL FORGET --
outcomes:
  can't tell      120
  not recalled    18
probe that retrieved the token (0 recall-success cells):
  R3 involved in 0 of 0
same conversation (rows) against new-conversation outcome (columns), 118 typed-erasure cells:
  recoverability        can't tell
  same_conversation_r1            
  FOUND                         68
  NOT FOUND                     50

===== perplexity =====
-- MASTER --
outcomes:
  not recalled    6
  can't tell      4
  recall failed   2
probe that retrieved the token (0 recall-success cells):
  R3 involved in 0 of 0
same conversation (rows) against new-conversation outcome (columns), 2 typed-erasure cells:
  recoverability        can't tell
  same_conversation_r1            
  NOT FOUND                      2
main-grid cells:
  PE-I1-E5     Clear all memories             R1=NOT RECALLED R2=NOT RECALLED R3=NOT RECALLED -> not recalled
  PE-I2-E5     Clear all memories             R1=NOT RECALLED R2=NOT RECALLED R3=NOT RECALLED -> not recalled
  PE-I1-E3     Delete all threads             R1=NOT FOUND R2=nan R3=NOT FOUND -> can't tell
  PE-I2-E3     Delete all threads             R1=NOT FOUND R2=nan R3=NOT FOUND -> recall failed
  PE-I1-E4     Delete individual memory       R1=NOT RECALLED R2=NOT RECALLED R3=NOT RECALLED -> not recalled
  PE-I2-E4     Delete individual memory       R1=NOT RECALLED R2=NOT RECALLED R3=NOT RECALLED -> not recalled
  PE-I1-E2     Delete single thread           R1=NOT FOUND R2=nan R3=NOT FOUND -> can't tell
  PE-I2-E2     Delete single thread           R1=NOT FOUND R2=nan R3=NOT FOUND -> recall failed
  PE-I1-E6     MAXIMAL                        R1=NOT RECALLED R2=NOT RECALLED R3=NOT RECALLED -> not recalled
  PE-I2-E6     MAXIMAL                        R1=NOT RECALLED R2=NOT RECALLED R3=NOT RECALLED -> not recalled
  PE-I1-E1     NL forget prompt               R1=NOT FOUND R2=nan R3=NOT FOUND -> can't tell
  PE-I2-E1     NL forget prompt               R1=NOT FOUND R2=nan R3=NOT FOUND -> can't tell
original token retrieved after replacement: 0

-- NL FORGET --
outcomes:
  can't tell      102
  recall success  31
  not recalled    5
probe that retrieved the token (31 recall-success cells):
  found by R1                                                  29
  token surfaced in a sibling cell's recall (sibling rule)     2
  R3 involved in 0 of 31
same conversation (rows) against new-conversation outcome (columns), 133 typed-erasure cells:
  recoverability        can't tell  recall success
  same_conversation_r1                            
  FOUND                         31              23
  NOT FOUND                     71               8

```
