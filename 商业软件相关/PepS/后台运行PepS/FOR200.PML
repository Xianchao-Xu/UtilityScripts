IDEN JB=1 CD=7 GR=-y IU=0 OU=0 PL=/Test Plant/                                  
TITL BL=3 GL=1 CV=4 HS=1 TI=/Test File/                                         
                                                                                
FREQ RF=101 FR=25 MP=33 MX=99 RP=0 EM=1                                         
                                                                                
LCAS CA=101 TY=0 EQ=6 TI=/PRESSURE/                                             
LCAS CA=102 TY=0 EQ=6 TI=/PRESSURE/                                             
LCAS CA=103 TY=0 EQ=6 TI=/PRESSURE/                                             
                                                                                
* MATERIAL: SA 213/312 TP316L                                                   
* (16 Cr 12 Ni 2 Mo)                                                            
*****************************                                                   
MATH CD=101 EX=2 TY=4 TX=650 TA=21 KL=1                                         
MATD TE=20  EH=200 EX=15.3 SM=127 SY=190   *SU=480                              
MATD TE=50  EH=197 EX=15.5                 *SU=455                              
MATD TE=100 EH=193 EX=15.9 SM=127 SY=165   *SU=430                              
MATD TE=150 EH=189 EX=16.2 SM=127 SY=150   *SU=410                              
MATD TE=200 EH=185 EX=16.6 SM=123 SY=137   *SU=390                              
MATD TE=250 EH=180 EX=16.9 SM=114 SY=127   *SU=385                              
MATD TE=300 EH=176 EX=17.2 SM=102 SY=113   *SU=380                              
MATD TE=350 EH=172 EX=17.5 SM=89  SY=99    *SU=380                              
MATD TE=400 EH=168 EX=17.8 SM=87  SY=97    *SU=380                              
MATD TE=450 EH=164 EX=18.0 SM=84  SY=93    *SU=370                              
MATD TE=500 EH=159 EX=18.3 SM=80  SY=89    *SU=360                              
MATD TE=550 EH=155 EX=18.5 SM=77  SY=86    *SU=350                              
MATD TE=600 EH=151 EX=18.7                 *SU=340                              
MATD TE=650 EH=147 EX=18.9                 *SU=330                              
MATL CD=101                                                                     
                                                                                
* CROSS SECTIONS                                                                
****************                                                                
CROS CD=1 OD=273.05 WT=9.271 MA=78.3 SO=0 ST=0 IN=0             *10" Sch 40S/STD
CROS CD=2 OD=219.07 WT=3.76 MA=25.77 SO=0 ST=1 IN=40 KL=1   *8" Sch 10S*        
CROS CD=3 OD=88.90  WT=3.05 MA=6.46  SO=1 ST=1                    *3" Sch 10S*  
CROS CD=4 OD=60.32  WT=3.91 MA=7.9   SO=0.854 ST=1 IN=40 KL=1   *2" Sch 40 Std 4
CROS CD=5 OD=48.26  WT=5.08 MA=7.62  SO=0.854 ST=1 IN=40 KL=1   *1"1/2 Sch 80 XS
CROS CD=6 OD=26.67  WT=2.87 MA=3.44  SO=0.854 ST=1 IN=40 KL=1   *3/4" Sch 40 Std
                                                                                
*                                                                               
DESN TE=650 PR=15.5                                                             
OPER CA=101 TE=250 PR=5.0                                                       
OPER CA=102 TE=450 PR=6.5                                                       
OPER CA=103 TE=575 PR=4.5                                                       
                                                                                
* MAIN LINE                                                                     
***********                                                                     
CROS CD=1                                                                       
ANCH PT=90                                                                      
TANG PT=100 DX=0.33 DZ=0.5715                                                   
BEND PT=120 X1=0.1905 Z1=0.33 Y2=-0.381                                         
TANG PT=130 EW=1 DY=-1.5                                                        
TANG PT=140 DY=-0.2032 *10" x 8" - Branch*                                      
TANG PT=150 EW=1 DY=-0.2032 *10" x 8" - Branch*                                 
TANG PT=160 EW=2 DY=-2                                                          
BEND PT=170 EW=2 Y1=-0.381 X2=0.381                                             
TANG PT=C001 DX=1.25                                                            
TANG PT=180 DX=1.25                                                             
ANCH PT=180                                                                     
JUNC PT=140                                                                     
BRAN PT=A140 EW=1 TE=2 DZ=0.2032 *10" x 8" - Branch*                            
TANG PT=C002 DZ=1.25                                                            
TANG PT=A141 DZ=1.25 EW=1                                                       
CRED PT=A142 EW=1 DZ=0.1524 *8" x 3"...6"*                                      
CROS CD=3                                                                       
TANG PT=A143 EW=1 DZ=0.9                                                        
TANG PT=A144 DZ=0.9                                                             
*FORC PT=A144 CA=101 FZ=10                                                      
BEND PT=A145 EW=1 Z1=0.076 X2=0.076                                             
*FORC PT=A145 CA=101 FX=-10                                                     
TANG PT=C003 DX=0.65                                                            
TANG PT=A146 DX=0.65                                                            
TANG PT=C004 DX=1                                                               
TANG PT=A150 DX=1                                                               
ANCH PT=A150                                                                    
CROS CD=2                                                                       
JUNC PT=C002                                                                    
BRAN PT=B140 DX=-1.25 TE=1                                                      
TANG PT=B141 DX=-1.25                                                           
ANCH PT=B141                                                                    
CROS CD=6                                                                       
JUNC PT=A146                                                                    
BRAN PT=D146 DZ=0.4 TE=0                                                        
TANG PT=D147 DZ=0.4                                                             
ANCH PT=D147                                                                    
                                                                                
ENDP                                                                            
