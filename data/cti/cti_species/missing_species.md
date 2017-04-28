This file lists eight species that cannot find atom composition from papers.

We list the reactions they involve and calculate their atoms using reaction balance.

If there is CanteraError about reaction balance, we can use this file to check it.



# species(name='PCHP2',atoms='C:1 H:1 O:0')

#### Reaction 61

reaction('2 RADIOM2 => 2 PCH2OH + 2 PCHP2 + 2 PCHOHP + 2 PH2 + C10H2M4 + 2 PCOH', [3.16E+07, 0, 83720])

#### Reaction 65

reaction('2 RKETM2 => 2 PCHP2 + 2 PCH2OH + 2 PH2 + C10H2M4 + 4 PCOH', [3.16E+07, 0, 83720])

#### Reaction 66

reaction('PRFET3M2 + PRFET3M2 => 2 PCOH + C10H2M4 + 2 PCHP2 + 2 PCHO + 2 PCHOHP + PH2', [3.16E+07, 0, 83720])

#### Reaction 78

reaction('2 RKET => 3 PCOH + 2 PCHP2 + 2 PCH2OH + PCOS + C#0H2 + 2 H2 + 2 PH2', [3.16E+07, 0, 83720])

#### Reaction 79

reaction('PRFET3 + PRFET3 => 2 PCHP2 + 2 PCHO + 2 PCHOHP + 2 PCOS + C10H2 + H2 + 2 PH2', [3.16E+07, 0, 83720])

#### Reaction 80

reaction('RLIGH + RLIGH => 2 PCOHP2 + 4 H2O + 2 PC2H2 + 4 PCOH + 2 C10H2M4 + H2 + 2 PCH3 + 2 PCHP2 + 2 PCH2P', [3.16E+07, 0, 83720])

#### Reaction 103

reaction('PCH2P[C:1, H:2] => PCHP2 + 0.5 H2[H:1]', [5.00E+08, 0, 209300])

#### Reaction 104

reaction('PCHP2 => 0.1 CHAR + 0.5 H2', [5.00E+08, 0, 209300])

#### Reaction 110

reaction('2 PRADIO => PCOH + PCOS + 2 PCH2OH + 2 PCHP2 + 2 PCHOHP + C10H2 + 2 PH2 + H2', [3.16E7, 0, 92092])

#### Reaction 111

reaction('2 PRADIOM2 => 2 PCOH + 2 PCH2OH + 2 PCHP2 + 2 PCHOHP + PH2 + C10H2M4', [3.16E7, 0, 83720])

# species(name='PH2',atoms='C:0 H:1 O:0')

#### Reaction 97

reaction('PH2 => H2', [1.00E+10, 0, 209300])

PH2:  H:1

H2:   H:2



# species(name='PCH3',atoms='C:1 H:3 O:0')

#### Reaction 102

reaction('PCH3 => RCH3[C:1 H:3]', [1.00E+13, 0, 125580])



# species(name='PRLIGH',atoms='C:22 H:27 O:9')

#### Reaction 1

reaction('PLIGH => PRLIGH', [1.00E+13, 0, 163254])

#### Reaction 118

reaction('PRLIGH + LIGH => PLIGH + RLIGH', [2*10**8.5, 0, 41860-4186])





# species(name='PRLIGH2',atoms='C:22 H:27 O:9')

#### Reaction 14

reaction('PRLIGH2 => PRLIGM2A + ALD3', [1.00E+13, 0, 133952])

#### Reaction 134

reaction('RC3H5O2 + PLIGH => C3H6O2 + PRLIGH2', [2*10**8, 0, 71162-4186])

#### Reaction 135

reaction('PRFET3 + PLIGH => PFET3 + PRLIGH2', [2*10**8, 0, 54418-4186])

#### Reaction 136

reaction('RC3H7O2 + PLIGH => C3H8O2 + PRLIGH2', [2*10**8, 0, 62790-4186])



# species(name='RMGUAI',atoms='C:8 H:9 O:3')

#### Reaction 15

reaction('RADIOM2 => RMGUAI + C3H6O2', [1.00E+13, 0, 133952])

#### Reaction 18

reaction('RLIGM2B => RMGUAI + PFET3M2', [1.00E+13, 0, 163254])

#### Reaction 64

reaction('2 RMGUAI => 2 PH2 + C10H2M4 + 2 PCOH', [3.16E+07, 0, 83720])

#### Reaction 129

reaction('RMGUAI + LIGH => MGUAI + RLIGH', [2*10**8, 0, 54418-4186])



# species(name='RLIGH',atoms='C:22 H:28 O:9')

#### Reaction 13

reaction('RLIGH => RLIGM2A + ALD3', [1.00E+13, 0, 133952])

#### Reaction 118

reaction('PRLIGH + LIGH => PLIGH + RLIGH', [2*10**8.5, 0, 41860-4186])



# species(name='PCOHP2',atoms='C:1 H:1 O:1')

#### Reaction 101

reaction('PCOHP2 => OH + 0.1 CHAR', [5.00E+08, 0, 0])

