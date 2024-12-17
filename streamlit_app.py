import streamlit as st
import pandas as pd
import CoolProp.CoolProp as CP
import numpy as np
#。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。函数。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。
def lambdaCalc(input_n,input_pi,input_pC,input_rhoSuc,V_Dis,file_name):   #计算压缩机的容积效率
    import pandas as pd
    import CoolProp.CoolProp as CP
    import numpy as np
    df = pd.read_excel('Messdata.xlsx',sheet_name=file_name)
    tC=df.iloc[:,0].values
    t0=df.iloc[:,1].values
    speed=df.iloc[:,2].values
    Pel=df.iloc[:,3].values
    etaInv=df.iloc[:,4].values
    tRoom=df.iloc[:,5].values
    tSuc=df.iloc[:,6].values
    tDis=df.iloc[:,7].values
    tShellTop=df.iloc[:,8].values
    tShellBottom=df.iloc[:,9].values
    m_flow_gh=df.iloc[:,10].values
    pC=CP.PropsSI('P','T',tC+273.15,'Q',0,'R600a')
    p0=CP.PropsSI('P','T',t0+273.15,'Q',0,'R600a')
    t=np.array(tSuc+273.15)
    p=np.array(p0)
    hIn=CP.PropsSI('H','T',t,'P',p,'R600a')
    t1=np.array(tSuc+273.15)
    p1=np.array(p0)
    p2=(pC)
    s=CP.PropsSI('S','T',t1,'P',p1,'R600a')
    hIs_pC=CP.PropsSI('H','S',s,'P',p2,'R600a')
    Pis=m_flow_gh/3600000*(hIs_pC-hIn)
    pi=pC/p0
    rhoSuc=CP.PropsSI('D','T',t1,'P',p1,'R600a')
    flowFactor=rhoSuc*speed/60
    V_flow=m_flow_gh/3600000/rhoSuc
    V_flowTheo=V_Dis*speed/60
    lamda=V_flow/V_flowTheo
    PelMotor=Pel/etaInv
    etaIs=Pis/PelMotor
    nDataPoints=len(tC)
    param_nRhoLarge=1e6
    param_piExp=2
    lamda=lamda.reshape((-1,1))
    pi=pi.reshape((-1,1))
    speed=(speed.reshape((-1,1)))
    pC=pC.reshape((-1,1))
    rhoSuc=rhoSuc.reshape((-1,1))
    inputData=np.hstack((lamda,pi,speed,pC,rhoSuc))
    fpi=np.zeros((nDataPoints,1))
    piStar=np.zeros((nDataPoints,1))
    speed1=speed/60
    speed2=speed1**2
    A=np.zeros((nDataPoints,8))
    for i in range(nDataPoints):
        fpi[i][0]=1+((speed[i][0]/60*rhoSuc[i][0])/param_nRhoLarge)**param_piExp
        piStar[i][0]=pi[i][0]*fpi[i][0]
        A[i,0]=1
        A[i,1]=piStar[i][0]
        A[i,2]=speed1[i][0]
        A[i,3]=pC[i][0]
        A[i,4]=speed2[i][0]
        A[i,5]=speed[i][0]*piStar[i][0]
        A[i,6]=speed[i][0]*rhoSuc[i][0]
        A[i,7]=pC[i][0]*piStar[i][0]   
    y=lamda
    c,residuals,rank,s=np.linalg.lstsq(A,y,rcond=None)
    input_fpi=1+((input_n*input_rhoSuc)/param_nRhoLarge)**param_piExp
    input_piStar=input_fpi*input_pi
    B=np.array([1,input_piStar,
    input_n,
    input_pC,
    (input_n)**2,
    input_n*input_piStar,
    input_n*input_rhoSuc,
    input_pC*input_piStar])
    B=B.reshape(1,-1)
    Lambda=np.dot(B,c)
    return (Lambda[0][0])
def etaIsCalc1(input_n,input_hIn,input_Pis,input_pi,input_dTSat,V_Dis,file_name):    #计算压缩机等熵效率
    import pandas as pd
    import CoolProp.CoolProp as CP
    import numpy as np
    df = pd.read_excel('Messdata.xlsx',sheet_name=file_name)
    tC=df.iloc[:,0].values
    t0=df.iloc[:,1].values
    speed=df.iloc[:,2].values
    Pel=df.iloc[:,3].values
    etaInv=df.iloc[:,4].values
    tRoom=df.iloc[:,5].values
    tSuc=df.iloc[:,6].values
    tDis=df.iloc[:,7].values
    tShellTop=df.iloc[:,8].values
    tShellBottom=df.iloc[:,9].values
    m_flow_gh=df.iloc[:,10].values
    pC=CP.PropsSI('P','T',tC+273.15,'Q',0,'R600a')
    p0=CP.PropsSI('P','T',t0+273.15,'Q',0,'R600a')
    t=np.array(tSuc+273.15)
    p=np.array(p0)
    hIn=CP.PropsSI('H','T',t,'P',p,'R600a')
    t1=np.array(tSuc+273.15)
    p1=np.array(p0)
    p2=(pC)
    s=CP.PropsSI('S','T',t1,'P',p1,'R600a')
    hIs_pC=CP.PropsSI('H','S',s,'P',p2,'R600a')
    Pis=m_flow_gh/3600000*(hIs_pC-hIn)      # 压缩机测试数据中流量单位为g/h，需换算成kg/s
    pi=pC/p0
    rhoSuc=CP.PropsSI('D','T',t1,'P',p1,'R600a')
    flowFactor=rhoSuc*speed/60              # 压缩机测试数据中转速单位为RPM，需换算成每秒
    V_flow=m_flow_gh/3600000/rhoSuc
    V_flowTheo=V_Dis*speed/60               # 压缩机测试数据中转速单位为RPM，需换算成每秒
    lamda=V_flow/V_flowTheo
    PelMotor=Pel/etaInv
    etaIs=Pis/PelMotor
    nDataPoints=len(tC)
    param_nRhoLarge=1e6
    param_piExp=2
    
    lamda=lamda.reshape((-1,1))
    pi=pi.reshape((-1,1))
    speed=(speed.reshape((-1,1)))
    pC=pC.reshape((-1,1))
    rhoSuc=rhoSuc.reshape((-1,1))
    inputData=np.hstack((lamda,pi,speed,pC,rhoSuc))

    etaIs=etaIs.reshape((-1,1))
    hIn=hIn.reshape((-1,1))
    Pis=Pis.reshape((-1,1))
    dTSat=tC-t0
    dTSat=dTSat.reshape((-1,1))

    inputData=np.hstack((etaIs,hIn,speed,pi,Pis,dTSat))
    speed1=speed/60                       # 压缩机测试数据中转速单位为RPM，需换算成每秒
    speed2=speed1**2

    A2=np.zeros((nDataPoints,8))
    for i in range(nDataPoints):
        A2[i,0]=1
        A2[i,1]=hIn[i][0]
        A2[i,2]=speed1[i][0]
        A2[i,3]=speed2[i][0]
        A2[i,4]=pi[i][0]
        A2[i,5]=Pis[i][0]
        A2[i,6]=Pis[i][0]*Pis[i][0]
        A2[i,7]=dTSat[i][0]
    
    y2=etaIs
    c2,residuals,rank,s=np.linalg.lstsq(A2,y2,rcond=None)

    B2=np.array([1,input_hIn,input_n,(input_n)**2,input_pi,input_Pis,input_Pis**2,input_dTSat],dtype=object)
    B2=B2.reshape(1,-1)
    etaIs=np.dot(B2,c2)
    return (etaIs[0][0])
def etaIsCalc2(input_n,input_Pis,input_pi,input_dTSat,V_Dis,file_name):   # 计算压缩机等熵效率，未拟合回气焓值
    import pandas as pd
    import CoolProp.CoolProp as CP
    import numpy as np
    df = pd.read_excel('Messdata.xlsx',sheet_name=file_name)
    tC=df.iloc[:,0].values      #行向量
    t0=df.iloc[:,1].values
    speed=df.iloc[:,2].values
    Pel=df.iloc[:,3].values
    etaInv=df.iloc[:,4].values
    tRoom=df.iloc[:,5].values
    tSuc=df.iloc[:,6].values
    tDis=df.iloc[:,7].values
    tShellTop=df.iloc[:,8].values
    tShellBottom=df.iloc[:,9].values
    m_flow_gh=df.iloc[:,10].values          # 压缩机实验测得的实际制冷剂流量
    pC=CP.PropsSI('P','T',tC+273.15,'Q',0,'R600a')
    p0=CP.PropsSI('P','T',t0+273.15,'Q',0,'R600a')
    #t=np.array(tSuc+273.15)
    #p=np.array(p0)
    hIn=CP.PropsSI('H','T',np.array(tSuc+273.15),'P',np.array(p0),'R600a')    # 回气点的焓值
    s=CP.PropsSI('S','T',np.array(tSuc+273.15),'P',np.array(p0),'R600a')
    rhoSuc=CP.PropsSI('D','T',np.array(tSuc+273.15),'P',np.array(p0),'R600a')
    #t1=np.array(tSuc+273.15)
    #p1=np.array(p0)
    #p2=(pC)
    
    hIs_pC=CP.PropsSI('H','S',s,'P',np.array(pC),'R600a')
    Pis=m_flow_gh/3600000*(hIs_pC-hIn)
 
    pi=pC/p0
        
    V_flow=m_flow_gh/3600000/rhoSuc
    V_flowTheo=V_Dis*speed/60         # 理论制冷剂流量
    lamda=V_flow/V_flowTheo           # 容积效率计算
    PelMotor=Pel/etaInv
    etaIs=Pis/PelMotor                # 等熵效率
    nDataPoints=len(tC)               # 统计实验数据组

    lamda=lamda.reshape((-1,1))       # 固定一列,行自动算,即转换成列向量
    pi=pi.reshape((-1,1))
    speed=(speed.reshape((-1,1)))
    pC=pC.reshape((-1,1))
    rhoSuc=rhoSuc.reshape((-1,1))
    #inputData=np.hstack((lamda,pi,speed,pC,rhoSuc))
 
    etaIs=etaIs.reshape((-1,1))
    hIn=hIn.reshape((-1,1))
    Pis=Pis.reshape((-1,1))
    dTSat=tC-t0
    dTSat=dTSat.reshape((-1,1))
    #inputData=np.hstack((etaIs,hIn,speed,pi,Pis,dTSat))
    speed1=speed/60
    speed2=speed1**2
 
    A2=np.zeros((nDataPoints,7))
    for i in range(nDataPoints):
        A2[i,0]=1
        A2[i,1]=speed1[i][0]
        A2[i,2]=speed2[i][0]
        A2[i,3]=pi[i][0]
        A2[i,4]=Pis[i][0]
        A2[i,5]=Pis[i][0]*Pis[i][0]
        A2[i,6]=dTSat[i][0]
    y2=etaIs
    c2,residuals,rank,s=np.linalg.lstsq(A2,y2,rcond=None)
    B2=np.array([1,input_n,(input_n)**2,input_pi,input_Pis,input_Pis**2,input_dTSat],dtype=object)
    B2=B2.reshape(1,-1)
    etaIs=np.dot(B2,c2)
    
    return (etaIs[0][0])
def etaInv_VarSpeed(input_n,input_PelMotor,input_tAmb,V_Dis,file_name):   # 计算压缩机变频器效率
    import pandas as pd
    import CoolProp.CoolProp as CP
    import numpy as np
    df = pd.read_excel('Messdata.xlsx',sheet_name=file_name)
    tC=df.iloc[:,0].values
    t0=df.iloc[:,1].values
    speed=df.iloc[:,2].values
    Pel=df.iloc[:,3].values
    etaInv=df.iloc[:,4].values
    tRoom=df.iloc[:,5].values
    tSuc=df.iloc[:,6].values
    tDis=df.iloc[:,7].values
    tShellTop=df.iloc[:,8].values
    tShellBottom=df.iloc[:,9].values
    m_flow_gh=df.iloc[:,10].values
    pC=CP.PropsSI('P','T',tC+273.15,'Q',0,'R600a')
    p0=CP.PropsSI('P','T',t0+273.15,'Q',0,'R600a')
    t=np.array(tSuc+273.15)
    p=np.array(p0)
    hIn=CP.PropsSI('H','T',t,'P',p,'R600a')
    t1=np.array(tSuc+273.15)
    p1=np.array(p0)
    p2=(pC)
    s=CP.PropsSI('S','T',t1,'P',p1,'R600a')
    hIs_pC=CP.PropsSI('H','S',s,'P',p2,'R600a')
    Pis=m_flow_gh/3600000*(hIs_pC-hIn)

    pi=pC/p0
    rhoSuc=CP.PropsSI('D','T',t1,'P',p1,'R600a')
    flowFactor=rhoSuc*speed/60
    V_flow=m_flow_gh/3600000/rhoSuc
    V_flowTheo=V_Dis*speed/60
    lamda=V_flow/V_flowTheo
    PelMotor=Pel/etaInv
    etaIs=Pis/PelMotor
    nDataPoints=len(tC)
    param_nRhoLarge=1e6
    param_piExp=2
    
    lamda=lamda.reshape((-1,1))
    pi=pi.reshape((-1,1))
    speed=(speed.reshape((-1,1)))
    pC=pC.reshape((-1,1))
    rhoSuc=rhoSuc.reshape((-1,1))
    PelMotor=PelMotor.reshape((-1,1))
    tRoom=tRoom.reshape((-1,1))

    etaIs=etaIs.reshape((-1,1))
    hIn=hIn.reshape((-1,1))
    Pis=Pis.reshape((-1,1))
    dTSat=tC-t0
    dTSat=dTSat.reshape((-1,1))
    speed1=speed/60

    A3=np.zeros((nDataPoints,7))
    for i in range(nDataPoints):
        A3[i,0]=1
        A3[i,1]=PelMotor[i][0]
        A3[i,2]=PelMotor[i][0]*PelMotor[i][0]
        A3[i,3]=1/PelMotor[i][0]
        A3[i,4]=speed1[i][0]
        A3[i,5]=speed1[i][0]*speed1[i][0]
        A3[i,6]=tRoom[i][0]
    
    y3=etaInv
    c3,residuals,rank,s=np.linalg.lstsq(A3,y3,rcond=None)

    B3=np.array([1,input_PelMotor,input_PelMotor**2,1/input_PelMotor,input_n,input_n**2,input_tAmb],dtype=object)
    B3=B3.reshape(1,-1)
    etaInv=np.dot(B3,c3)

    return (etaInv)

#。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。网页。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。
st.title("🎈 Compressor COP calculation")
# 输入
compressor_name = st.text_input("Compressor Name", value="VESH11C_20567_r")
V_Dis = st.number_input("V_Dis (cm3)", value=10)/1000000
T_evap = st.number_input("Evaporating Temperature (°C)", value=-25.0)
T_cond = st.number_input("Condensing Temperature (°C)", value=35.0)
tSuc = st.number_input("Suction Temperature (°C)", value=25.0)
nCompressor = st.number_input("Compressor Speed (RPM)", value=1500.0)/60
if st.button("Calculate COP"):
    # 计算逻辑
    p0 =CP.PropsSI('P','T',T_evap +273.15,'Q',0,'R600a')
    pc =CP.PropsSI('P','T',T_cond +273.15,'Q',0,'R600a')
    pi =pc /p0 
    #低压端饱和气态点6，过热（回气）点1
    h6 =CP.PropsSI('H','T',T_evap +273.15,'Q',1,'R600a')
    h1 =CP.PropsSI('H','T',tSuc +273.15,'P',p0 ,'R600a')
    rhoSuc =CP.PropsSI('D','T',tSuc +273.15,'P',p0 ,'R600a')
    #得到容积效率和质量流量    
    lamda =lambdaCalc(nCompressor ,pi ,pc ,rhoSuc ,V_Dis,compressor_name)
    lvn =lamda *V_Dis*nCompressor
    m_flow =lvn *rhoSuc 
    #高压端饱和液态点3,低压端入口点4
    h3 =CP.PropsSI('H','T',T_cond +273.15,'Q',0,'R600a')
    h4 =h3
    Q0 =m_flow *(h1 -h4 )
    s =CP.PropsSI('S','T',tSuc +273.15,'P',p0 ,'R600a')
    h2_Is =CP.PropsSI('H','S',s ,'P',pc ,'R600a')               
    Pis =m_flow *(h2_Is -h1 )
    dTSat =T_cond -T_evap 
    etaIs =etaIsCalc1(nCompressor ,h1 ,Pis ,pi ,dTSat ,V_Dis,compressor_name)
    h2 =h1 +(h2_Is -h1 )/etaIs 
    Qc =m_flow *(h2 -h3 ) 
    P_el=Pis/etaIs
    COP=Q0/P_el
    st.write(f"COP={COP}")
    st.write(f"Pel={P_el}")
    st.write(f"Q0={Q0}")

