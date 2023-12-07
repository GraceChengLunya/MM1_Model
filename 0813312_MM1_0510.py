import random
import simpy
Customer_Count = 0
Customer_leaveQueue_Count = 0
Total_Waiting_Time = 0
Customer_arriveQueue_time = []
Customer_leaveQueue_time = []
wait_timeList = []
Qnow=0
# Source to generate job arrivals
def source(env, job_type, number_jobs, inter_arrival_time, processing_time, processor, QC):
    for i in range(number_jobs):
        # Job arrival event: Generating a new job 
        global Customer_Count                       ###計算已生成的物件數
        Customer_Count += 1
        global Qnow
        if Qnow<QC:
            Qnow = Qnow + 1
        global Customer_arriveQueue_time            ###將抵達時間存入list
        Customer_arriveQueue_time.append(env.now)
        global Customer_leaveQueue_time             ###預設離開時間為1000
        Customer_leaveQueue_time.append(1000)
        #print('    The', job_type, 'Job%1d arrived at %1.0f' % (i+1,env.now))
        c = processing(env, job_type, 'Job%1d' % (i+1), processor, processing_time,i)  ###加一個參數i用以控制物件
        env.process(c)                      
        duration = random.expovariate(1.0 / inter_arrival_time)
        yield env.timeout(duration)         # Waiting for generating the next job  

                

# Processor or resource to process job request
def processing(env, job_type, job_id, processor, processing_time,number_Of_Job):  ###加一個number_Of_Job的參數用以控制list
    arrive = env.now  #arrive at queue的時間
        
    with processor.request() as req: 
        yield req                        # Waiting for processing 
        global Customer_leaveQueue_Count ###計算多少個物件已離開queue
        Customer_leaveQueue_Count += 1
        global Qnow
        Qnow= Qnow-1
        
        global Customer_leaveQueue_time  ###更新離開queue的時間
        Customer_leaveQueue_time[number_Of_Job] = env.now
        wait_time = Customer_leaveQueue_time[number_Of_Job] - Customer_arriveQueue_time[number_Of_Job]
        global wait_timeList
        wait_timeList.append(wait_time)  ###計算各個物件的等待時間
        global Total_Waiting_Time
        Total_Waiting_Time += wait_timeList[number_Of_Job]
        # Job starts processing
        #print('    The', job_type, job_id, 'starts processing at %1.0f' % env.now)                                
        duration = random.expovariate(1.0 / processing_time)                        
        yield env.timeout(duration)      # Processing 
        #print('    The', job_type, job_id, 'has finished processing at %1.0f' % env.now) 



# Start simulation
print('# Simulation Start ###########################################################')
RANDOM_SEED = 813312
random.seed(RANDOM_SEED)

for k in range(3):
    for t in range (100):
        Customer_Count = 0
        Customer_leaveQueue_Count = 0
        Total_Waiting_Time = 0
        Qnow=0
        QC=10+5*k
        Customer_arriveQueue_time = []
        Customer_leaveQueue_time = []
        wait_timeList = []
        env = simpy.Environment()
        processor = simpy.Resource(env, capacity=1)
        env.process(source(env,job_type='JobType_A', number_jobs = 1000, inter_arrival_time=10, processing_time=8, processor=processor, QC=QC))
        env.run(until=1000)
        if(Customer_Count > Customer_leaveQueue_Count):   ###將未處理的物件的等待時間加入
               for i in range(Customer_leaveQueue_Count,Customer_Count):
                   Total_Waiting_Time += (Customer_leaveQueue_time[i] - Customer_arriveQueue_time[i]) ###這裡要用i不能i+1 ，因為陣列從0開始
                   i += 1
        #print('# Simulatio End ###########################################################')
        #print(f"生產的物件總數:{Customer_Count}")
        #print(f"離開queue的物件數:{Customer_leaveQueue_Count}")
        #print(f"the last Item arrive time:{Customer_arriveQueue_time[Customer_Count-1]}")
        #print(f"the last Item leave queue time:{Customer_leaveQueue_time[Customer_Count-1]}")
        #print(f"Total Waiting Time:{Total_Waiting_Time}")
        print(f"{Total_Waiting_Time/Customer_Count}")


