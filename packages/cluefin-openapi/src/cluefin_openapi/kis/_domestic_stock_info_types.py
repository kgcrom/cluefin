from pydantic import BaseModel
from typing import Sequence, Optional
from pydantic import Field
from cluefin_openapi.kis._models import KisHttpBody

pdno	상품번호	string	Y	12
prdt_type_cd	상품유형코드	string	Y	3
prdt_name	상품명	string	Y	60
prdt_name120	상품명120	string	Y	120
prdt_abrv_name	상품약어명	string	Y	60
prdt_eng_name	상품영문명	string	Y	60
prdt_eng_name120	상품영문명120	string	Y	120
prdt_eng_abrv_name	상품영문약어명	string	Y	60
std_pdno	표준상품번호	string	Y	12
shtn_pdno	단축상품번호	string	Y	12
prdt_sale_stat_cd	상품판매상태코드	string	Y	2
prdt_risk_grad_cd	상품위험등급코드	string	Y	2
prdt_clsf_cd	상품분류코드	string	Y	6
prdt_clsf_name	상품분류명	string	Y	60
sale_strt_dt	판매시작일자	string	Y	8
sale_end_dt	판매종료일자	string	Y	8
wrap_asst_type_cd	랩어카운트자산유형코드	string	Y	2
ivst_prdt_type_cd	투자상품유형코드	string	Y	4
ivst_prdt_type_cd_name	투자상품유형코드명	string	Y	60
frst_erlm_dt	최초등록일자	string	Y	8
class ProductBasicInfoItem(BaseModel):
    pass


class ProductBasicInfo(BaseModel):
    """상품기본조회"""

    output: ProductBasicInfoItem = Field(title="응답상세")

pdno	상품번호	string	Y	12	 
prdt_type_cd	상품유형코드	string	Y	3	 
mket_id_cd	시장ID코드	string	Y	3	<description>AGR.농축산물파생
BON.채권파생
CMD.일반상품시장
CUR.통화파생
ENG.에너지파생
EQU.주식파생
ETF.ETF파생
IRT.금리파생
KNX.코넥스
KSQ.코스닥
MTL.금속파생
SPI.주가지수파생
STK.유가증권</description>
scty_grp_id_cd	증권그룹ID코드	string	Y	2	<description> BC.수익증권
DR.주식예탁증서
EF.ETF
EN.ETN
EW.ELW
FE.해외ETF
FO.선물옵션
FS.외국주권
FU.선물
FX.플렉스 선물
GD.금현물
IC.투자계약증권
IF.사회간접자본투융자회사
KN.코넥스주권
MF.투자회사
OP.옵션
RT.부동산투자회사
SC.선박투자회사
SR.신주인수권증서
ST.주권
SW.신주인수권증권
TC.신탁수익증권</description>
excg_dvsn_cd	거래소구분코드	string	Y	2	<description> 01.한국증권
02.증권거래소
03.코스닥
04.K-OTC
05.선물거래소
06.CME
07.EUREX
21.금현물
50.미국주간
51.홍콩
52.상해B
53.심천
54.홍콩거래소
55.미국
56.일본
57.상해A
58.심천A
59.베트남
61.장전시간외시장
64.경쟁대량매매
65.경매매시장
81.시간외단일가시장</description>
setl_mmdd	결산월일	string	Y	4	 
lstg_stqt	상장주수	string	Y	19	 
lstg_cptl_amt	상장자본금액	string	Y	19	 
cpta	자본금	string	Y	19	 
papr	액면가	string	Y	19	 
issu_pric	발행가격	string	Y	19	 
kospi200_item_yn	코스피200종목여부	string	Y	1	 
scts_mket_lstg_dt	유가증권시장상장일자	string	Y	8	 
scts_mket_lstg_abol_dt	유가증권시장상장폐지일자	string	Y	8	 
kosdaq_mket_lstg_dt	코스닥시장상장일자	string	Y	8	 
kosdaq_mket_lstg_abol_dt	코스닥시장상장폐지일자	string	Y	8	 
frbd_mket_lstg_dt	프리보드시장상장일자	string	Y	8	 
frbd_mket_lstg_abol_dt	프리보드시장상장폐지일자	string	Y	8	 
reits_kind_cd	리츠종류코드	string	Y	1	 
etf_dvsn_cd	ETF구분코드	string	Y	2	 
oilf_fund_yn	유전펀드여부	string	Y	1	 
idx_bztp_lcls_cd	지수업종대분류코드	string	Y	3	 
idx_bztp_mcls_cd	지수업종중분류코드	string	Y	3	 
idx_bztp_scls_cd	지수업종소분류코드	string	Y	3	 
stck_kind_cd	주식종류코드	string	Y	3	<description> 000.해당사항없음
101.보통주
201.우선주
202.2우선주
203.3우선주
204.4우선주
205.5우선주
206.6우선주
207.7우선주
208.8우선주
209.9우선주
210.10우선주
211.11우선주
212.12우선주
213.13우선주
214.14우선주
215.15우선주
216.16우선주
217.17우선주
218.18우선주
219.19우선주
220.20우선주
301.후배주
401.혼합주</description>
mfnd_opng_dt	뮤추얼펀드개시일자	string	Y	8	 
mfnd_end_dt	뮤추얼펀드종료일자	string	Y	8	 
dpsi_erlm_cncl_dt	예탁등록취소일자	string	Y	8	 
etf_cu_qty	ETFCU수량	string	Y	10	 
prdt_name	상품명	string	Y	60	 
prdt_name120	상품명120	string	Y	120	 
prdt_abrv_name	상품약어명	string	Y	60	 
std_pdno	표준상품번호	string	Y	12	 
prdt_eng_name	상품영문명	string	Y	60	 
prdt_eng_name120	상품영문명120	string	Y	120	 
prdt_eng_abrv_name	상품영문약어명	string	Y	60	 
dpsi_aptm_erlm_yn	예탁지정등록여부	string	Y	1	 
etf_txtn_type_cd	ETF과세유형코드	string	Y	2	 
etf_type_cd	ETF유형코드	string	Y	2	 
lstg_abol_dt	상장폐지일자	string	Y	8	 
nwst_odst_dvsn_cd	신주구주구분코드	string	Y	2	 
sbst_pric	대용가격	string	Y	19	 
thco_sbst_pric	당사대용가격	string	Y	19	 
thco_sbst_pric_chng_dt	당사대용가격변경일자	string	Y	8	 
tr_stop_yn	거래정지여부	string	Y	1	 
admn_item_yn	관리종목여부	string	Y	1	 
thdt_clpr	당일종가	string	Y	19	 
bfdy_clpr	전일종가	string	Y	19	 
clpr_chng_dt	종가변경일자	string	Y	8	 
std_idst_clsf_cd	표준산업분류코드	string	Y	6	 
std_idst_clsf_cd_name	표준산업분류코드명	string	Y	130	<description>표준산업소분류코드</description>
000000	해당사항없음                                     
010101	작물 재배업                                      
010102	축산업                                           
010103	작물재배 및 축산 복합농업                        
010104	작물재배 및 축산 관련 서비스업                   
010105	수렵 및 관련 서비스업                            
010201	임업                                             
010301	어로 어업                                        
010302	양식어업 및 어업관련 서비스업                    
020501	석탄 광업                                        
020502	원유 및 천연가스 채굴업                          
020601	철 광업                                          
020602	비철금속 광업                                    
020701	토사석 광업                                      
020702	기타 비금속광물 광업                             
020801	광업 지원 서비스업                               
031001	도축, 육류 가공 및 저장 처리업                   
031002	수산물 가공 및 저장 처리업                       
031003	과실, 채소 가공 및 저장 처리업                   
031004	동물성 및 식물성 유지 제조업                     
031005	낙농제품 및 식용빙과류 제조업                    
031006	곡물가공품, 전분 및 전분제품 제조업              
031007	기타 식품 제조업                                 
031008	동물용 사료 및 조제식품 제조업                   
031101	알콜음료 제조업                                  
031102	비알콜음료 및 얼음 제조업                        
031201	담배 제조업                                      
031301	방적 및 가공사 제조업                            
031302	직물직조 및 직물제품 제조업                      
031303	편조원단 및 편조제품 제조업                      
031304	섬유제품 염색, 정리 및 마무리 가공업             
031309	기타 섬유제품 제조업                             
031401	봉제의복 제조업                                  
031402	모피가공 및 모피제품 제조업                      
031403	편조의복 제조업                                  
031404	의복 액세서리 제조업                             
031501	가죽, 가방 및 유사제품 제조업                    
031502	신발 및 신발부분품 제조업                        
031601	제재 및 목재 가공업                              
031602	나무제품 제조업                                  
031603	코르크 및 조물 제품 제조업                       
031701	펄프, 종이 및 판지 제조업                        
031702	골판지, 종이 상자 및 종이용기 제조업             
031709	기타 종이 및 판지 제품 제조업                    
031801	인쇄 및 인쇄관련 산업                            
031802	기록매체 복제업                                  
031901	코크스 및 연탄 제조업                            
031902	석유 정제품 제조업                               
032001	기초화학물질 제조업                              
032002	비료 및 질소화합물 제조업                        
032003	합성고무 및 플라스틱 물질 제조업                 
032004	기타 화학제품 제조업                             
032005	화학섬유 제조업                                  
032101	기초 의약물질 및 생물학적 제제 제조업            
032102	의약품 제조업                                    
032103	의료용품 및 기타 의약관련제품 제조업             
032201	고무제품 제조업                                  
032202	플라스틱제품 제조업                              
032301	유리 및 유리제품 제조업                          
032302	도자기 및 기타 요업제품 제조업                   
032303	시멘트, 석회, 플라스터 및 그 제품 제조업         
032309	기타 비금속 광물제품 제조업                      
032401	1차 철강 제조업                                  
032402	1차 비철금속 제조업                              
032403	금속 주조업                                      
032501	구조용 금속제품, 탱크 및 증기발생기 제조업       
032502	무기 및 총포탄 제조업                            
032509	기타 금속가공제품 제조업                         
032601	반도체 제조업                                    
032602	전자부품 제조업                                  
032603	컴퓨터 및 주변장치 제조업                        
032604	통신 및 방송 장비 제조업                         
032605	영상 및 음향기기 제조업                          
032606	마그네틱 및 광학 매체 제조업                     
032701	의료용 기기 제조업                               
032702	측정, 시험, 항해, 제어 및 기타 정밀기기 제조업; ?
032703	안경, 사진장비 및 기타 광학기기 제조업           
032704	시계 및 시계부품 제조업                          
032801	전동기, 발전기 및 전기 변환 · 공급 · 제어 장치 
032802	일차전지 및 축전지 제조업                        
032803	절연선 및 케이블 제조업                          
032804	전구 및 조명장치 제조업                          
032805	가정용 기기 제조업                               
032809	기타 전기장비 제조업                             
032901	일반 목적용 기계 제조업                          
032902	특수 목적용 기계 제조업                          
033001	자동차용 엔진 및 자동차 제조업                   
033002	자동차 차체 및 트레일러 제조업                   
033003	자동차 부품 제조업                               
033101	선박 및 보트 건조업                              
033102	철도장비 제조업                                  
033103	항공기,우주선 및 부품 제조업                     
033109	그외 기타 운송장비 제조업                        
033201	가구 제조업                                      
033301	귀금속 및 장신용품 제조업                        
033302	악기 제조업                                      
033303	운동 및 경기용구 제조업                          
033304	인형,장난감 및 오락용품 제조업                   
033309	그외 기타 제품 제조업                            
043501	전기업                                           
043502	가스 제조 및 배관공급업                          
043503	증기, 냉온수 및 공기조절 공급업                  
043601	수도사업                                         
053701	하수, 폐수 및 분뇨 처리업                        
053801	폐기물 수집운반업                                
053802	폐기물 처리업                                    
053803	금속 및 비금속 원료 재생업                       
053901	환경 정화 및 복원업                              
064101	건물 건설업                                      
064102	토목 건설업                                      
064201	기반조성 및 시설물 축조관련 전문공사업           
064202	건물설비 설치 공사업                             
064203	전기 및 통신 공사업                              
064204	실내건축 및 건축 마무리 공사업                   
064205	건설장비 운영업                                  
074501	자동차 판매업                                    
074502	자동차 부품 및 내장품 판매업                     
074503	모터사이클 및 부품 판매업                        
074601	상품 중개업                                      
074602	산업용 농축산물 및 산동물 도매업                 
074603	음·식료품 및 담배 도매업                        
074604	가정용품 도매업                                  
074605	기계장비 및 관련 물품 도매업                     
074606	건축자재, 철물 및 난방장치 도매업                
074607	기타 전문 도매업                                 
074608	상품 종합 도매업                                 
074701	종합 소매업                                      
074702	음·식료품 및 담배 소매업                        
074703	정보통신장비 소매업                              
074704	섬유, 의복, 신발 및 가죽제품 소매업              
074705	기타 가정용품 소매업                             
074706	문화, 오락 및 여가 용품 소매업                   
074707	연료 소매업                                      
074708	기타 상품 전문 소매업                            
074709	무점포 소매업                                    
084901	철도운송업                                       
084902	육상 여객 운송업                                 
084903	도로 화물 운송업                                 
084904	소화물 전문 운송업                               
084905	파이프라인 운송업                                
085001	해상 운송업                                      
085002	내륙 수상 및 항만내 운송업                       
085101	정기 항공 운송업                                 
085102	부정기 항공 운송업                               
085201	보관 및 창고업                                   
085209	기타 운송관련 서비스업                           
095501	숙박시설 운영업                                  
095509	기타 숙박업                                      
095601	음식점업                                         
095602	주점 및 비알콜음료점업                           
105801	서적, 잡지 및 기타 인쇄물 출판업                 
105802	소프트웨어 개발 및 공급업                        
105901	영화, 비디오물, 방송프로그램 제작 및 배급업      
105902	오디오물 출판 및 원판 녹음업                     
106001	라디오 방송업                                    
106002	텔레비전 방송업                                  
106101	우편업                                           
106102	전기통신업                                       
106201	컴퓨터 프로그래밍, 시스템 통합 및 관리업         
106301	자료처리, 호스팅, 포털 및 기타 인터넷 정보매개서?
106309	기타 정보 서비스업                               
116401	은행 및 저축기관                                 
116402	투자기관                                         
116409	기타 금융업                                      
116501	보험업                                           
116502	재 보험업                                        
116503	연금 및 공제업                                   
116601	금융지원 서비스업                                
116602	보험 및 연금관련 서비스업                        
126801	부동산 임대 및 공급업                            
126802	부동산 관련 서비스업                             
126901	운송장비 임대업                                  
126902	개인 및 가정용품 임대업                          
126903	산업용 기계 및 장비 임대업                       
126904	무형재산권 임대업                                
137001	자연과학 및 공학 연구개발업                      
137002	인문 및 사회과학 연구개발업                      
137101	법무관련 서비스업                                
137102	회계 및 세무관련 서비스업                        
137103	광고업                                           
137104	시장조사 및 여론조사업                           
137105	회사본부, 지주회사 및 경영컨설팅 서비스업        
137201	건축기술, 엔지니어링 및 관련기술 서비스업        
137209	기타 과학기술 서비스업                           
137301	수의업                                           
137302	전문디자인업                                     
137303	사진 촬영 및 처리업                              
137309	그외 기타 전문, 과학 및 기술 서비스업            
147401	사업시설 유지관리 서비스업                       
147402	건물·산업설비 청소 및 방제 서비스업             
147403	조경 관리 및 유지 서비스업                       
147501	인력공급 및 고용알선업                           
147502	여행사 및 기타 여행보조 서비스업                 
147503	경비, 경호 및 탐정업                             
147509	기타 사업지원 서비스업                           
158401	입법 및 일반 정부 행정                           
158402	사회 및 산업정책 행정                            
158403	외무 및 국방 행정                                
158404	사법 및 공공질서 행정                            
158405	사회보장 행정                                    
168501	초등 교육기관                                    
168502	중등 교육기관                                    
168503	고등 교육기관                                    
168504	특수학교, 외국인학교 및 대안학교                 
168505	일반 교습 학원                                   
168506	기타 교육기관                                    
168507	교육지원 서비스업                                
178601	병원                                             
178602	의원                                             
178603	공중 보건 의료업                                 
178609	기타 보건업                                      
178701	거주 복지시설 운영업                             
178702	비거주 복지시설 운영업                           
189001	창작 및 예술관련 서비스업                        
189002	도서관, 사적지 및 유사 여가관련 서비스업         
189101	스포츠 서비스업                                  
189102	유원지 및 기타 오락관련 서비스업                 
199401	산업 및 전문가 단체                              
199402	노동조합                                         
199409	기타 협회 및 단체                                
199501	기계 및 장비 수리업                              
199502	자동차 및 모터사이클 수리업                      
199503	개인 및 가정용품 수리업                          
199601	미용, 욕탕 및 유사 서비스업                      
199609	그외 기타 개인 서비스업                          
209701	가구내 고용활동                                  
209801	자가 소비를 위한 가사 생산 활동                  
209802	자가 소비를 위한 가사 서비스 활동                
219901	국제 및 외국기관  </description>
idx_bztp_lcls_cd_name	지수업종대분류코드명	string	Y	60	<description> 표준산업대분류코드
00	해당사항없음                                                            
01	농업, 임업 및 어업                                                      
02	광업                                                                    
03	제조업                                                                  
04	전기, 가스, 증기 및 수도사업                                            
05	하수-폐기물 처리, 원료재생 및환경복원업                                 
06	건설업                                                                  
07	도매 및 소매업                                                          
08	운수업                                                                  
09	숙박 및 음식점업                                                        
10	출판, 영상, 방송통신 및 정보서비스업                                    
11	금융 및 보험업                                                          
12	부동산업 및 임대업                                                      
13	전문, 과학 및 기술 서비스업                                             
14	사업시설관리 및 사업지원서비스업                                        
15	공공행정, 국방 및 사회보장 행정                                         
16	교육 서비스업                                                           
17	보건업 및 사회복지 서비스업                                             
18	예술, 스포츠 및 여가관련 서비스업                                       
19	협회 및 단체, 수리 및 기타 개인 서비스업                                
20	가구내 고용활동 및 달리 분류되지 않은 자가소비생산활동                  
21	국제 및 외국기관 </description>
idx_bztp_mcls_cd_name	지수업종중분류코드명	string	Y	60	<description>표준산업중분류코드                                                   
0000	해당사항없음                                                            
0101	농업                                                                    
0102	임업                                                                    
0103	어업                                                                    
0205	석탄, 원유 및 천연가스 광업                                             
0206	금속 광업                                                               
0207	비금속광물 광업; 연료용 제외                                            
0208	광업 지원 서비스업                                                      
0310	식료품 제조업                                                           
0311	음료 제조업                                                             
0312	담배 제조업                                                             
0313	섬유제품 제조업; 의복제외                                               
0314	의복, 의복액세서리 및 모피제품제조업                                    
0315	가죽, 가방 및 신발 제조업                                               
0316	목재 및 나무제품 제조업;가구제외                                        
0317	펄프, 종이 및 종이제품 제조업                                           
0318	인쇄 및 기록매체 복제업                                                 
0319	코크스, 연탄 및 석유정제품 제조업                                       
0320	화학물질 및 화학제품 제조업;의약품 제외                                 
0321	의료용 물질 및 의약품 제조업                                            
0322	고무제품 및 플라스틱제품 제조업                                         
0323	비금속 광물제품 제조업                                                  
0324	1차 금속 제조업                                                         
0325	금속가공제품 제조업;기계 및가구 제외                                    
0326	전자부품, 컴퓨터, 영상, 음향 및 통신장비 제조업                         
0327	의료, 정밀, 광학기기 및 시계 제조업                                     
0328	전기장비 제조업                                                         
0329	기타 기계 및 장비 제조업                                                
0330	자동차 및 트레일러 제조업                                               
0331	기타 운송장비 제조업                                                    
0332	가구 제조업                                                             
0333	기타 제품 제조업                                                        
0435	전기, 가스, 증기 및 공기조절 공급업                                     
0436	수도사업                                                                
0537	하수, 폐수 및 분뇨 처리업                                               
0538	폐기물 수집운반, 처리 및 원료재생업                                     
0539	환경 정화 및 복원업                                                     
0641	종합 건설업                                                             
0642	전문직별 공사업                                                         
0745	자동차 및 부품 판매업                                                   
0746	도매 및 상품중개업                                                      
0747	소매업; 자동차 제외                                                     
0849	육상운송 및 파이프라인 운송업                                           
0850	수상 운송업                                                             
0851	항공 운송업                                                             
0852	창고 및 운송관련 서비스업                                               
0955	숙박업                                                                  
0956	음식점 및 주점업                                                        
1058	출판업                                                                  
1059	영상·오디오 기록물 제작 및 배급업                                      
1060	방송업                                                                  
1061	통신업                                                                  
1062	컴퓨터 프로그래밍, 시스템 통합및 관리업                                 
1063	정보서비스업                                                            
1164	금융업                                                                  
1165	보험 및 연금업                                                          
1166	금융 및 보험 관련 서비스업                                              
1268	부동산업                                                                
1269	임대업;부동산 제외                                                      
1370	연구개발업                                                              
1371	전문서비스업                                                            
1372	건축기술, 엔지니어링 및 기타과학기술 서비스업                           
1373	기타 전문, 과학 및 기술 서비스업                                        
1474	사업시설 관리 및 조경 서비스업                                          
1475	사업지원 서비스업                                                       
1584	공공행정, 국방 및 사회보장 행정                                         
1685	교육 서비스업                                                           
1786	보건업                                                                  
1787	사회복지 서비스업                                                       
1890	창작, 예술 및 여가관련 서비스업                                         
1891	스포츠 및 오락관련 서비스업                                             
1994	협회 및 단체                                                            
1995	수리업                                                                  
1996	기타 개인 서비스업                                                      
2097	가구내 고용활동                                                         
2098	달리 분류되지 않은 자가소비를 위한가구의 재화 및 서비스 생산활동        
2199	국제 및 외국기관     </description>
idx_bztp_scls_cd_name	지수업종소분류코드명	string	Y	60	 표준산업소분류코드 참조
ocr_no	OCR번호	string	Y	4	 
crfd_item_yn	크라우드펀딩종목여부	string	Y	1	 
elec_scty_yn	전자증권여부	string	Y	1	 
issu_istt_cd	발행기관코드	string	Y	5	 
etf_chas_erng_rt_dbnb	ETF추적수익율배수	string	Y	19	 
etf_etn_ivst_heed_item_yn	ETFETN투자유의종목여부	string	Y	1	 
stln_int_rt_dvsn_cd	대주이자율구분코드	string	Y	2	 
frnr_psnl_lmt_rt	외국인개인한도비율	string	Y	24	 
lstg_rqsr_issu_istt_cd	상장신청인발행기관코드	string	Y	5	 
lstg_rqsr_item_cd	상장신청인종목코드	string	Y	12	 
trst_istt_issu_istt_cd	신탁기관발행기관코드	string	Y	5	 
cptt_trad_tr_psbl_yn	NXT 거래종목여부	string	Y	1	NXT 거래가능한 종목은 Y, 그 외 종목은 N
nxt_tr_stop_yn	NXT 거래정지여부	string	Y	1	NXT 거래종목 중 거래정지가 된 종목은 Y, 그 외 모든 종목은 N
class StockBasicInfoItem(BaseModel):
    pass


class StockBasicInfo(BaseModel):
    """주식기본조회"""

    output: StockBasicInfoItem = Field(title="응답상세")


stac_yymm	결산 년월	string	Y	6	 
cras	유동자산	string	Y	112	 
fxas	고정자산	string	Y	112	 
total_aset	자산총계	string	Y	102	 
flow_lblt	유동부채	string	Y	112	 
fix_lblt	고정부채	string	Y	112	 
total_lblt	부채총계	string	Y	102	 
cpfn	자본금	string	Y	22	 
cfp_surp	자본 잉여금	string	Y	182	출력되지 않는 데이터(99.99 로 표시)
prfi_surp	이익 잉여금	string	Y	182	출력되지 않는 데이터(99.99 로 표시)
total_cptl	자본총계	string	Y	102	 
class BalanceSheetItem(BaseModel):
    pass


class BalanceSheet(BaseModel):
    """국내주식 대차대조표"""

    output: Sequence[BalanceSheetItem] = Field(default_factory=list)

stac_yymm	결산 년월	string	Y	6	 
sale_account	매출액	string	Y	18	 
sale_cost	매출 원가	string	Y	182	 
sale_totl_prfi	매출 총 이익	string	Y	182	 
depr_cost	감가상각비	string	Y	182	출력되지 않는 데이터(99.99 로 표시)
sell_mang	판매 및 관리비	string	Y	182	출력되지 않는 데이터(99.99 로 표시)
bsop_prti	영업 이익	string	Y	182	 
bsop_non_ernn	영업 외 수익	string	Y	182	출력되지 않는 데이터(99.99 로 표시)
bsop_non_expn	영업 외 비용	string	Y	182	출력되지 않는 데이터(99.99 로 표시)
op_prfi	경상 이익	string	Y	182	 
spec_prfi	특별 이익	string	Y	182	 
spec_loss	특별 손실	string	Y	182	 
thtr_ntin	당기순이익	string	Y	102	 
class IncomeStatementItem(BaseModel):
    pass


class IncomeStatement(BaseModel):
    """국내주식 손익계산서"""

    output: Sequence[IncomeStatementItem] = Field(default_factory=list)


stac_yymm	결산 년월	string	Y	6	 
grs	매출액 증가율	string	Y	124	 
bsop_prfi_inrt	영업 이익 증가율	string	Y	124	 적자지속, 흑자전환, 적자전환인 경우 0으로 표시
ntin_inrt	순이익 증가율	string	Y	124	 
roe_val	ROE 값	string	Y	132	 
eps	EPS	string	Y	112	 
sps	주당매출액	string	Y	18	 
bps	BPS	string	Y	112	 
rsrv_rate	유보 비율	string	Y	84	 
lblt_rate	부채 비율	string	Y	84	 
class FinancialRatioItem(BaseModel):
    pass


class FinancialRatio(BaseModel):
    """국내주식 재무비율"""

    output: Sequence[FinancialRatioItem] = Field(default_factory=list)


stac_yymm	결산 년월	string	Y	6
cptl_ntin_rate	총자본 순이익율	string	Y	92
self_cptl_ntin_inrt	자기자본 순이익율	string	Y	92
sale_ntin_rate	매출액 순이익율	string	Y	92
sale_totl_rate	매출액 총이익율	string	Y	92
class ProfitabilityRatioItem(BaseModel):
    pass


class ProfitabilityRatio(BaseModel):
    """국내주식 수익성비율"""

    output: Sequence[ProfitabilityRatioItem] = Field(default_factory=list)

stac_yymm	결산 년월	string	Y	6	 
payout_rate	배당 성향	string	Y	92	비정상 출력되는 데이터로 무시
eva	EVA	string	Y	82	 
ebitda	EBITDA	string	Y	82	 
ev_ebitda	EV_EBITDA	string	Y	82
class OtherKeyRatioItem(BaseModel):
    pass


class OtherKeyRatio(BaseModel):
    """국내주식 기타주요비율"""

    output: Sequence[OtherKeyRatioItem] = Field(default_factory=list)


stac_yymm	결산 년월	string	Y	6
lblt_rate	부채 비율	string	Y	84
bram_depn	차입금 의존도	string	Y	92
crnt_rate	유동 비율	string	Y	84
quck_rate	당좌 비율	string	Y	84
class StabilityRatioItem(BaseModel):
    pass


class StabilityRatio(BaseModel):
    """국내주식 안정성비율"""

    output: Sequence[StabilityRatioItem] = Field(default_factory=list)


stac_yymm	결산 년월	string	Y	6
grs	매출액 증가율	string	Y	124
bsop_prfi_inrt	영업 이익 증가율	string	Y	124
equt_inrt	자기자본 증가율	string	Y	92
totl_aset_inrt	총자산 증가율	string	Y	92
class GrowthRatioItem(BaseModel):
    pass


class GrowthRatio(BaseModel):
    """국내주식 성장성비율"""

    output: Sequence[GrowthRatioItem] = Field(default_factory=list)


stck_shrn_iscd	주식 단축 종목코드	string	Y	9
hts_kor_isnm	HTS 한글 종목명	string	Y	40
crdt_rate	신용 비율	string	Y	84
class MarginTradableStocksItem(BaseModel):
    pass


class MarginTradableStocks(BaseModel):
    """국내주식 당사 신용가능종목"""

    output: Sequence[MarginTradableStocksItem] = Field(default_factory=list)

record_date	기준일	string	Y	8
sht_cd	종목코드	string	Y	9
isin_name	종목명	string	Y	40
divi_kind	배당종류	string	Y	8
face_val	액면가	string	Y	9
per_sto_divi_amt	현금배당금	string	Y	12
divi_rate	현금배당률(%)	string	Y	62
stk_divi_rate	주식배당률(%)	string	Y	152
divi_pay_dt	배당금지급일	string	Y	10
stk_div_pay_dt	주식배당지급일	string	Y	10
odd_pay_dt	단주대금지급일	string	Y	10
stk_kind	주식종류	string	Y	10
high_divi_gb	고배당종목여부	string	Y	1
class KsdDividendDecisionItem(BaseModel):
    pass


class KsdDividendDecision(BaseModel):
    """예탁원정보(배당결정)"""

    output: Sequence[KsdDividendDecisionItem] = Field(default_factory=list)

record_date	기준일	string	Y	8
sht_cd	종목코드	string	Y	9
isin_name	종목명	string	Y	40
stk_kind	주식종류	string	Y	8
opp_opi_rcpt_term	반대의사접수시한	string	Y	9
buy_req_rcpt_term	매수청구접수시한	string	Y	12
buy_req_price	 매수청구가격	string	Y	62
buy_amt_pay_dt	매수대금지급일	string	Y	62
get_meet_dt	주총일	string	Y	10
class KsdStockDividendDecisionItem(BaseModel):
    pass


class KsdStockDividendDecision(BaseModel):
    """예탁원정보(주식배수청구결정)"""

    output1: Sequence[KsdStockDividendDecisionItem] = Field(default_factory=list)


record_date	기준일	string	Y	8
sht_cd	종목코드	string	Y	9
opp_cust_cd	피합병(피분할)회사코드	string	Y	5
opp_cust_nm	피합병(피분할)회사명	string	Y	37
cust_cd	합병(분할)회사코드	string	Y	5
cust_nm	합병(분할)회사명	string	Y	37
merge_type	합병사유	string	Y	8
merge_rate	비율	string	Y	142
td_stop_dt	매매거래정지기간	string	Y	23
list_dt	상장/등록일	string	Y	9
odd_amt_pay_dt	단주대금지급일	string	Y	10
tot_issue_stk_qty	발행주식	string	Y	12
issue_stk_qty	발행할주식	string	Y	12
seq	연번	string	Y	3
class KsdMergerSplitDecisionItem(BaseModel):
    pass


class KsdMergerSplitDecision(BaseModel):
    """예탁원정보(합병/분할결정)"""

    output1: Sequence[KsdMergerSplitDecisionItem] = Field(default_factory=list)

record_date	기준일	string	Y	8
sht_cd	종목코드	string	Y	9
isin_name	종목명	string	Y	40
inter_bf_face_amt	변경전액면가	string	Y	9
inter_af_face_amt	변경후액면가	string	Y	9
td_stop_dt	매매거래정지기간	string	Y	23
list_dt	상장/등록일	string	Y	10
class KsdParValueChangeDecisionItem(BaseModel):
    pass


class KsdParValueChangeDecision(BaseModel):
    """예탁원정보(액면교체결정)"""

    output1: Sequence[KsdParValueChangeDecisionItem] = Field(default_factory=list)

record_date	기준일	string	Y	8
sht_cd	종목코드	string	Y	9
isin_name	종목명	string	Y	40
stk_kind	주식종류	string	Y	10
reduce_cap_type	감자구분	string	Y	9
reduce_cap_rate	감자배정율	string	Y	142
comp_way	계산방법	string	Y	6
td_stop_dt	매매거래정지기간	string	Y	23
list_dt	상장/등록일	string	Y	10
class KsdCapitalReductionScheduleItem(BaseModel):
    pass


class KsdCapitalReductionSchedule(BaseModel):
    """예탁원정보(자본감소일정)"""

    output1: Sequence[KsdCapitalReductionScheduleItem] = Field(default_factory=list)


list_dt	상장/등록일	string	Y	10
sht_cd	종목코드	string	Y	9
isin_name	종목명	string	Y	40
stk_kind	주식종류	string	Y	10
issue_type	사유	string	Y	21
issue_stk_qty	상장주식수	string	Y	12
tot_issue_stk_qty	총발행주식수	string	Y	12
issue_price	발행가	string	Y	9
class KsdListingInfoScheduleItem(BaseModel):
    pass


class KsdListingInfoSchedule(BaseModel):
    """예탁원정보(상장정보일정)"""

    output1: Sequence[KsdListingInfoScheduleItem] = Field(default_factory=list)


record_date	기준일	string	Y	8
sht_cd	종목코드	string	Y	9
isin_name	종목명	string	Y	40
fix_subscr_pri	공모가	string	Y	12
face_value	액면가	string	Y	9
subscr_dt	청약기간	string	Y	23
pay_dt	납입일	string	Y	10
refund_dt	환불일	string	Y	10
list_dt	상장/등록일	string	Y	10
lead_mgr	주간사	string	Y	41
pub_bf_cap	공모전자본금	string	Y	12
pub_af_cap	공모후자본금	string	Y	12
assign_stk_qty	당사배정물량	string	Y	12
class KsdIpoSubscriptionScheduleItem(BaseModel):
    pass


class KsdIpoSubscriptionSchedule(BaseModel):
    """예탁원정보(공모주청약일정)"""

    output1: Sequence[KsdIpoSubscriptionScheduleItem] = Field(default_factory=list)

record_date	기준일	string	Y	8
sht_cd	종목코드	string	Y	9
isin_name	종목명	string	Y	40
subscr_dt	청약일	string	Y	23
subscr_price	공모가	string	Y	9
subscr_stk_qty	공모주식수	string	Y	12
refund_dt	환불일	string	Y	10
list_dt	상장/등록일	string	Y	10
lead_mgr	주간사	string	Y	25
class KsdForfeitedShareScheduleItem(BaseModel):
    pass


class KsdForfeitedShareSchedule(BaseModel):
    """예탁원정보(실권주일정)"""

    output1: Sequence[KsdForfeitedShareScheduleItem] = Field(default_factory=list)


sht_cd	종목코드	string	Y	9
isin_name	종목명	string	Y	40
stk_qty	주식수	string	Y	12
depo_date	예치일	string	Y	23
depo_reason	사유	string	Y	10
tot_issue_qty_per_rate	총발행주식수대비비율(%)	string	Y	52
class KsdDepositScheduleItem(BaseModel):
    pass


class KsdDepositSchedule(BaseModel):
    """예탁원정보(입무예치일정)"""

    output1: Sequence[KsdDepositScheduleItem] = Field(default_factory=list)

record_date	기준일	string	Y	8
sht_cd	종목코드	string	Y	9
isin_name	종목명	string	Y	40
tot_issue_stk_qty	발행주식	string	Y	12
issue_stk_qty	발행할주식	string	Y	12
fix_rate	확정배정율	string	Y	152
disc_rate	할인율	string	Y	52
fix_price	발행예정가	string	Y	8
right_dt	권리락일	string	Y	8
sub_term_ft	청약기간	string	Y	8
sub_term	청약기간	string	Y	23
list_date	상장/등록일	string	Y	10
stk_kind	주식종류	string	Y	2
class KsdPaidInCapitalIncreaseScheduleItem(BaseModel):
    pass


class KsdPaidInCapitalIncreaseSchedule(BaseModel):
    """예탁원정보(유상증자일정)"""

    output: Sequence[KsdPaidInCapitalIncreaseScheduleItem] = Field(default_factory=list)

record_date	기준일	string	Y	8
sht_cd	종목코드	string	Y	9
isin_name	종목명	string	Y	40
fix_rate	확정배정율	string	Y	152
odd_rec_price	단주기준가	string	Y	9
right_dt	권리락일	string	Y	8
odd_pay_dt	단주대금지급일	string	Y	23
list_date	상장/등록일	string	Y	8
tot_issue_stk_qty	발행주식	string	Y	12
issue_stk_qty	발행할주식	string	Y	12
stk_kind	주식종류	string	Y	2
class KsdStockDividendScheduleItem(BaseModel):
    pass


class KsdStockDividendSchedule(BaseModel):
    """예탁원정보(무상증자일정)"""

    output1: Sequence[KsdStockDividendScheduleItem] = Field(default_factory=list)

record_date	기준일	string	Y	8
sht_cd	종목코드	string	Y	9
isin_name	종목명	string	Y	40
gen_meet_dt	주총일자	string	Y	10
gen_meet_type	주총사유	string	Y	8
agenda	주총의안	string	Y	71
vote_tot_qty	의결권주식총수	string	Y	12
class KsdShareholderMeetingScheduleItem(BaseModel):
    pass


class KsdShareholderMeetingSchedule(BaseModel):
    """예탁원정보(주주총회일정)"""

    output1: Sequence[KsdShareholderMeetingScheduleItem] = Field(default_factory=list)


sht_cd	ELW단축종목코드	string	Y	9
item_kor_nm	HTS한글종목명	string	Y	40
name1	ELW현재가	string	Y	10
name2	전일대비	string	Y	10
estdate	전일대비부호	string	Y	1
rcmd_name	전일대비율	string	Y	82
capital	누적거래량	string	Y	18
forn_item_lmtrt	행사가	string	Y	112
class EstimatedEarningsItem1(BaseModel):
    pass

data1	DATA1	string	Y	15	결산연월(outblock4) 참조
data2	DATA2	string	Y	15	결산연월(outblock4) 참조
data3	DATA3	string	Y	15	결산연월(outblock4) 참조
data4	DATA4	string	Y	15	결산연월(outblock4) 참조
data5	DATA5	string	Y	15	결산연월(outblock4) 참조
class EstimatedEarningsItem2(BaseModel):
    pass

data1	DATA1	string	Y	15	결산연월(outblock4) 참조
data2	DATA2	string	Y	15	결산연월(outblock4) 참조
data3	DATA3	string	Y	15	결산연월(outblock4) 참조
data4	DATA4	string	Y	15	결산연월(outblock4) 참조
data5	DATA5	string	Y	15	결산연월(outblock4) 참조
class EstimatedEarningsItem3(BaseModel):
    pass

dt	결산년월	string	Y	8	DATA1 ~5 결산월 정보
class EstimatedEarningsItem4(BaseModel):
    pass

class EstimatedEarnings(BaseModel, KisHttpBody):
    """국내주식 종목추정실적"""

    output1: EstimatedEarningsItem1 = Field(title="응답상세1")
    output2: Sequence[EstimatedEarningsItem2] = Field(default_factory=list)
    output3: Sequence[EstimatedEarningsItem3] = Field(default_factory=list)
    output4: Sequence[EstimatedEarningsItem4] = Field(default_factory=list)


pdno	상품번호	string	Y	12	 
prdt_name	상품명	string	Y	60	 
papr	액면가	string	Y	19	 
bfdy_clpr	전일종가	string	Y	19	전일종가
sbst_prvs	대용가	string	Y	19	 
tr_stop_dvsn_name	거래정지구분명	string	Y	60	 
psbl_yn_name	가능여부명	string	Y	60	 
lmt_qty1	한도수량1	string	Y	19	 
use_qty1	사용수량1	string	Y	19	 
trad_psbl_qty2	매매가능수량2	string	Y	19	가능수량
rght_type_cd	권리유형코드	string	Y	2	 
bass_dt	기준일자	string	Y	8	 
psbl_yn	가능여부	string	Y	1	 
class StockLoanableListItem1(BaseModel):
    pass

tot_stup_lmt_qty	총설정한도수량	string	Y	19
brch_lmt_qty	지점한도수량	string	Y	19
rqst_psbl_qty	신청가능수량	string	Y	19
class StockLoanableListItem2(BaseModel):
    pass

class StockLoanableList(BaseModel, KisHttpBody):
    """당사 대주가능 종목"""

    output1: Sequence[StockLoanableListItem1] = Field(default_factory=list)
    output2: StockLoanableListItem2 = Field(title="응답상세2")


stck_bsop_date	주식영업일자	string	Y	8
invt_opnn	투자의견	string	Y	40
invt_opnn_cls_code	투자의견구분코드	string	Y	2
rgbf_invt_opnn	직전투자의견	string	Y	40
rgbf_invt_opnn_cls_code	직전투자의견구분코드	string	Y	2
mbcr_name	회원사명	string	Y	50
hts_goal_prc	HTS목표가격	string	Y	10
stck_prdy_clpr	주식전일종가	string	Y	10
stck_nday_esdg	주식N일괴리도	string	Y	10
nday_dprt	N일괴리율	string	Y	82
stft_esdg	주식선물괴리도	string	Y	10
dprt	괴리율	string	Y	82
class InvestmentOpinionItem(BaseModel):
    pass


class InvestmentOpinion(BaseModel):
    """국내주식 종목투자의견"""

    output: Sequence[InvestmentOpinionItem] = Field(default_factory=list)


stck_bsop_date	주식영업일자	string	Y	8
stck_shrn_iscd	주식단축종목코드	string	Y	9
hts_kor_isnm	HTS한글종목명	string	Y	40
invt_opnn	투자의견	string	Y	40
invt_opnn_cls_code	투자의견구분코드	string	Y	2
rgbf_invt_opnn	직전투자의견	string	Y	40
rgbf_invt_opnn_cls_code	직전투자의견구분코드	string	Y	2
mbcr_name	회원사명	string	Y	50
stck_prpr	주식현재가	string	Y	10
prdy_vrss	전일대비	string	Y	10
prdy_vrss_sign	전일대비부호	string	Y	1
prdy_ctrt	전일대비율	string	Y	82
hts_goal_prc	HTS목표가격	string	Y	10
stck_prdy_clpr	주식전일종가	string	Y	10
stft_esdg	주식선물괴리도	string	Y	10
dprt	괴리율	string	Y	82
class InvestmentOpinionByBrokerageItem(BaseModel):
    pass


class InvestmentOpinionByBrokerage(BaseModel):
    """국내주식 증권사별 투자의견"""

    output: Sequence[InvestmentOpinionByBrokerageItem] = Field(default_factory=list)
