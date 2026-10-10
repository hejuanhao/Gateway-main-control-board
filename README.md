项目功能
该工程是基于 STM32F103C8T6 的消防监测网关固件。网关作为消防监测中心主控板，负责连接控制箱、地面监测站和天空端无人机，完成 LoRa 数据收发、上位机通信、节点状态解析、现场告警及 RS485 LED 屏显示。
系统启动后，LED屏显示三行设备状态：
1. 地面监测端一
2. 地面监测端二
3. 空中无人机一
网关可以从 USART1、RS485 或 LoRa 接收控制命令，并统一更新对应设备状态。任一设备出现火情或求助时，告警灯点亮；全部设备恢复正常后，告警灯关闭。
通信参数
接口	参数	用途
USART1	115200，8N1	网口模块、电脑或控制箱通信
USART2	9600，8N1	RS485 LED屏通信及命令接收
SPI1	约9 Mbit/s，Mode 0	驱动LoRa模块
LoRa	488 MHz、SF7、125 kHz、CR 4/7、20 dBm	地面站及无人机无线通信
MCU	72 MHz	数据解析与设备控制


命令格式
指令必须作为3个十六进制字节发送，不能发送ASCII字符串。
指令	功能
57 01 01	地面监测端一有火
57 01 00	地面监测端一正常
57 02 01	地面监测端二有火
57 02 00	地面监测端二正常
57 03 01	空中无人机一有火
57 03 00	空中无人机一正常
58 01 01	地面监测端一求助
58 02 01	地面监测端二求助
58 03 01	空中无人机一求助


使用方法
1. 使用 Keil MDK 打开 [testwg3.uvprojx](C:/Users/25546/Desktop/简历/项目：自研网关/wg three/wg three/testwg3/MDK-ARM/testwg3.uvprojx)。
2. 通过 ST-Link 和 SWD 接口连接主控板，编译后下载程序。
3. 连接 LoRa 模块、RS485 LED屏、网口模块及告警灯。
4. 上电后确认三行设备状态均显示“正常”。
5. 使用串口工具选择十六进制发送模式，通过 USART1 或 RS485 发送上述命令。
6. LoRa节点也可发送同样的3字节命令，网关接收后自动更新LED屏。
7. 观察LED屏对应行、告警灯和通信指示灯是否正确动作。
工程已生成可直接烧录的 [testwg3.hex](C:/Users/25546/Desktop/简历/项目：自研网关/wg three/wg three/testwg3/MDK-ARM/testwg3/testwg3.hex)，最新构建记录为 0 Error(s), 0 Warning(s)。核心业务位于 [main.c (line 314)](C:/Users/25546/Desktop/简历/项目：自研网关/wg three/wg three/testwg3/Core/Src/main.c:314)，LED屏协议帧可使用 [显示屏.py (line 1)](C:/Users/25546/Desktop/简历/项目：自研网关/wg three/wg three/显示屏.py:1) 生成。
气象百叶箱的数据采集应由地面监测站完成；当前网关工程主要接收地面站经LoRa上传的火情和状态结果，并未直接实现百叶箱Modbus轮询。
