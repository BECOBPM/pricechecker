<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>산업안전보건관리비 AI 자동 검토 대시보드</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;500;600;700;800&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {
            font-family: 'Pretendard', 'Inter', -apple-system, sans-serif;
            background-color: #f8fafc;
        }
        
        /* Custom scrollbar for table */
        .table-container::-webkit-scrollbar {
            height: 8px;
            width: 8px;
        }
        .table-container::-webkit-scrollbar-track {
            background: #f1f5f9; 
            border-radius: 4px;
        }
        .table-container::-webkit-scrollbar-thumb {
            background: #cbd5e1; 
            border-radius: 4px;
        }
        .table-container::-webkit-scrollbar-thumb:hover {
            background: #94a3b8; 
        }

        .status-badge {
            transition: all 0.2s ease;
        }
    </style>
</head>
<body class="text-slate-800 antialiased flex h-screen overflow-hidden">

    <!-- Sidebar -->
    <aside class="w-64 bg-slate-900 text-white flex-shrink-0 hidden md:flex flex-col border-r border-slate-800 shadow-xl">
        <div class="h-16 flex items-center px-6 border-b border-slate-800 bg-slate-950/60">
            <div class="w-9 h-9 rounded-xl bg-blue-600 flex items-center justify-center mr-3 shadow-lg shadow-blue-500/30">
                <i class="fa-solid fa-shield-halved text-white text-base"></i>
            </div>
            <div>
                <span class="text-base font-extrabold tracking-tight text-white block">SafeAI-Check</span>
                <span class="text-[10px] text-blue-400 font-semibold uppercase tracking-wider">산안비 정산 AI</span>
            </div>
        </div>

        <nav class="flex-1 px-4 py-6 space-y-1.5 overflow-y-auto">
            <a href="#" class="flex items-center px-4 py-3 bg-blue-600 text-white rounded-xl font-medium shadow-md shadow-blue-600/20">
                <i class="fa-solid fa-gauge-high w-5 mr-3 text-sm"></i>
                검토 대시보드
            </a>
            <a href="#" onclick="quickFilter('적합')" class="flex items-center px-4 py-3 text-slate-300 hover:bg-slate-800 hover:text-white rounded-xl transition font-medium">
                <i class="fa-solid fa-circle-check w-5 mr-3 text-emerald-400 text-sm"></i>
                적격 내역만 보기
            </a>
            <a href="#" onclick="quickFilter('부적합')" class="flex items-center px-4 py-3 text-slate-300 hover:bg-slate-800 hover:text-white rounded-xl transition font-medium">
                <i class="fa-solid fa-circle-xmark w-5 mr-3 text-rose-400 text-sm"></i>
                부적합(불인정) 목록
            </a>
            <a href="#" onclick="quickFilter('조건부')" class="flex items-center px-4 py-3 text-slate-300 hover:bg-slate-800 hover:text-white rounded-xl transition font-medium">
                <i class="fa-solid fa-triangle-exclamation w-5 mr-3 text-amber-400 text-sm"></i>
                한도·보완 필요 건
            </a>
        </nav>

        <!-- Legal Notice Tag -->
        <div class="p-4 mx-3 mb-4 rounded-xl bg-slate-800/80 border border-slate-700/60 text-[11px] text-slate-400 space-y-1">
            <div class="font-bold text-slate-200 flex items-center gap-1.5">
                <i class="fa-solid fa-scale-balanced text-blue-400"></i> 기준 법령
            </div>
            <p>고용노동부 고시 제2023-49호<br>「건설업 산업안전보건관리비 계상 및 사용기준」</p>
        </div>

        <div class="p-4 border-t border-slate-800/80 bg-slate-950/40">
            <div class="flex items-center">
                <div class="w-9 h-9 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center text-white font-black text-sm shadow">
                    안
                </div>
                <div class="ml-3 text-xs">
                    <p class="font-bold text-white">현장 안전총괄팀</p>
                    <p class="text-slate-400">admin@safety-audit.kr</p>
                </div>
            </div>
        </div>
    </aside>

    <!-- Main Content Area -->
    <main class="flex-1 flex flex-col h-full relative overflow-hidden bg-slate-50">
        
        <!-- Header -->
        <header class="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6 flex-shrink-0 shadow-sm z-10">
            <div class="flex items-center gap-3">
                <h1 class="text-base md:text-lg font-black text-slate-900 flex items-center gap-2">
                    산업안전보건관리비 AI 자동 검토 대시보드
                    <span class="text-xs bg-emerald-50 text-emerald-700 font-semibold px-2.5 py-0.5 rounded-full border border-emerald-200 hidden sm:inline-flex items-center gap-1">
                        <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span> 실시간 판정 활성화
                    </span>
                </h1>
            </div>
            <div class="flex items-center space-x-3">
                <button onclick="exportCSV()" class="text-xs bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 font-bold px-3 py-2 rounded-lg transition flex items-center gap-1.5 shadow-sm">
                    <i class="fa-solid fa-file-arrow-down text-emerald-600"></i> CSV 내보내기
                </button>
                <button onclick="window.print()" class="text-xs bg-slate-800 hover:bg-slate-900 text-white font-bold px-3 py-2 rounded-lg transition flex items-center gap-1.5 shadow-sm">
                    <i class="fa-solid fa-print"></i> 보고서 인쇄
                </button>
            </div>
        </header>

        <!-- Scrollable Content Body -->
        <div class="flex-1 overflow-y-auto p-4 md:p-6 space-y-6">
            <div class="max-w-6xl mx-auto space-y-6">
                
                <!-- Input & Registration Section -->
                <section class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
                    <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/60 flex items-center justify-between">
                        <h2 class="text-sm font-bold text-slate-800 flex items-center gap-2">
                            <i class="fa-solid fa-microchip text-blue-600"></i> 청구 품목 분석 (AI 고시 대조)
                        </h2>
                        <span class="text-[11px] text-slate-500 font-medium">영수증 품목명 및 세부 규격 입력</span>
                    </div>

                    <div class="p-6 space-y-4">
                        <div class="grid grid-cols-1 md:grid-cols-12 gap-3 items-end">
                            <div class="md:col-span-8">
                                <label for="expenseItem" class="block text-xs font-bold text-slate-700 mb-1.5">
                                    구매/집행 품목 내역 입력 <span class="text-rose-500">*</span>
                                </label>
                                <div class="relative">
                                    <input type="text" id="expenseItem" 
                                           class="block w-full pl-4 pr-10 py-3 text-sm bg-white border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition shadow-sm text-slate-900 placeholder:text-slate-400" 
                                           placeholder="예: KCs 인증 안전모, 시스템 비계 임대, 이동식 AI CCTV, 도로 신호수, 제빙기, 회식비 등" 
                                           onkeypress="handleKeyPress(event)">
                                    <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none text-slate-400">
                                        <i class="fa-solid fa-magnifying-glass text-xs"></i>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="md:col-span-4 flex gap-2 w-full">
                                <button onclick="triggerFileSelect()" class="flex-1 flex items-center justify-center px-4 py-3 bg-white border border-slate-300 rounded-xl text-slate-700 hover:bg-slate-50 transition shadow-sm text-xs font-bold gap-2">
                                    <i class="fa-solid fa-camera text-slate-500"></i>
                                    <span id="uploadBtnLabel">증빙 사진</span>
                                </button>
                                <input type="file" id="fileUpload" class="hidden" accept="image/*" onchange="handleFileChange(event)">
                                
                                <button onclick="analyzeInput()" class="flex-1 flex items-center justify-center px-5 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl transition shadow-md shadow-blue-500/20 text-xs font-bold gap-1.5">
                                    <i class="fa-solid fa-wand-magic-sparkles"></i> AI 검토 실행
                                </button>
                            </div>
                        </div>

                        <!-- Quick Test Keywords Pills -->
                        <div class="pt-2 flex flex-wrap items-center gap-2 text-xs">
                            <span class="text-slate-400 font-semibold mr-1">빠른 예시:</span>
                            <button onclick="setSample('KCs 인증 용접 안전장갑')" class="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg transition font-medium">안전장갑</button>
                            <button onclick="setSample('외부 도장용 시스템 비계 임대')" class="px-2.5 py-1 bg-rose-50 hover:bg-rose-100 text-rose-700 rounded-lg transition font-medium">시스템 비계</button>
                            <button onclick="setSample('지능형 스마트 AI CCTV 관제 카메라')" class="px-2.5 py-1 bg-blue-50 hover:bg-blue-100 text-blue-700 rounded-lg transition font-medium">스마트 AI CCTV</button>
                            <button onclick="setSample('도로 점용 및 토사 반출 교통 신호수 인건비')" class="px-2.5 py-1 bg-amber-50 hover:bg-amber-100 text-amber-700 rounded-lg transition font-medium">교통 신호수</button>
                            <button onclick="setSample('폭염 대비 현장 근로자용 제빙기 렌탈')" class="px-2.5 py-1 bg-purple-50 hover:bg-purple-100 text-purple-700 rounded-lg transition font-medium">폭염 제빙기</button>
                            <button onclick="setSample('무재해 달성 축하 근로자 안전기원 회식비')" class="px-2.5 py-1 bg-rose-50 hover:bg-rose-100 text-rose-700 rounded-lg transition font-medium">회식비</button>
                        </div>
                    </div>
                </section>

                <!-- Results Table Section -->
                <section class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden flex flex-col">
                    <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/60 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                        <div class="flex items-center gap-3">
                            <h2 class="text-sm font-bold text-slate-800 flex items-center gap-2">
                                <i class="fa-solid fa-list-check text-blue-600"></i> 검토 결과 내역서
                            </h2>
                            <span class="text-xs font-bold px-2.5 py-0.5 bg-blue-50 text-blue-700 rounded-full border border-blue-200">
                                Total: <span id="itemCount">3</span>건
                            </span>
                        </div>

                        <!-- Table Filter Pills -->
                        <div class="flex items-center gap-1.5 text-xs">
                            <button onclick="filterTable('전체')" class="px-2.5 py-1 bg-slate-900 text-white rounded-lg font-bold filter-btn" data-filter="전체">전체</button>
                            <button onclick="filterTable('적합')" class="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg font-medium filter-btn" data-filter="적합">적합</button>
                            <button onclick="filterTable('부적합')" class="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg font-medium filter-btn" data-filter="부적합">부적합</button>
                            <button onclick="filterTable('조건부')" class="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg font-medium filter-btn" data-filter="조건부">조건부/검토필요</button>
                        </div>
                    </div>
                    
                    <div class="table-container overflow-x-auto w-full">
                        <table class="w-full text-left border-collapse">
                            <thead>
                                <tr class="bg-slate-50/80 text-slate-500 text-xs uppercase tracking-wider border-b border-slate-200">
                                    <th class="px-6 py-3.5 font-bold whitespace-nowrap">요청일시</th>
                                    <th class="px-6 py-3.5 font-bold">청구 품목 / 내역</th>
                                    <th class="px-6 py-3.5 font-bold text-center whitespace-nowrap">판정 결과</th>
                                    <th class="px-6 py-3.5 font-bold">AI 검토 근거 (고용노동부 고시 제7조 기준)</th>
                                </tr>
                            </thead>
                            <tbody id="resultTableBody" class="divide-y divide-slate-100 text-xs">
                                <!-- Preloaded Initial 3 Items -->
                                <tr class="hover:bg-slate-50 transition" data-status="적합">
                                    <td class="px-6 py-4 text-slate-500 whitespace-nowrap">2026-11-03 09:15</td>
                                    <td class="px-6 py-4 font-bold text-slate-900">
                                        KCs 인증 구조용 삼각대
                                        <div class="text-[11px] font-normal text-slate-400 mt-0.5">증빙: KCs안전인증표 등록됨</div>
                                    </td>
                                    <td class="px-6 py-4 text-center whitespace-nowrap">
                                        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-200 status-badge">
                                            <i class="fa-solid fa-circle-check mr-1 text-emerald-600"></i> 적합
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 text-slate-600">
                                        <strong class="text-slate-800">제7조 제1항 제3호(개인보호구 및 안전장구 구입비)</strong> - 추락방지 및 밀폐공간 구조용 장비는 근로자 직접 보호를 위해 산안비 적격 사용 가능합니다.
                                    </td>
                                </tr>

                                <tr class="hover:bg-slate-50 transition" data-status="부적합">
                                    <td class="px-6 py-4 text-slate-500 whitespace-nowrap">2026-11-03 09:05</td>
                                    <td class="px-6 py-4 font-bold text-slate-900">
                                        외부 도장용 시스템 비계 임대료
                                        <div class="text-[11px] font-normal text-rose-500 mt-0.5">※ 공사원가(직접비) 이관 대상</div>
                                    </td>
                                    <td class="px-6 py-4 text-center whitespace-nowrap">
                                        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-rose-100 text-rose-800 border border-rose-200 status-badge">
                                            <i class="fa-solid fa-circle-xmark mr-1 text-rose-600"></i> 부적합
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 text-slate-600">
                                        <strong class="text-rose-700">제7조 제2항(사용불가 가설시설물)</strong> - 작업 통로 및 발판을 겸하는 비계는 시공성 가설물이므로 직접공사비(공통가설비) 대상입니다. 산안비 청구 시 환수 대상입니다.
                                    </td>
                                </tr>

                                <tr class="hover:bg-slate-50 transition" data-status="부적합">
                                    <td class="px-6 py-4 text-slate-500 whitespace-nowrap">2026-11-03 08:30</td>
                                    <td class="px-6 py-4 font-bold text-slate-900">
                                        현장 작업팀 안전기원 회식비
                                    </td>
                                    <td class="px-6 py-4 text-center whitespace-nowrap">
                                        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-rose-100 text-rose-800 border border-rose-200 status-badge">
                                            <i class="fa-solid fa-circle-xmark mr-1 text-rose-600"></i> 부적합
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 text-slate-600">
                                        <strong class="text-rose-700">제7조 제2항(사용불가 복리후생비)</strong> - 사기진작, 친목도모, 복리후생 목적의 식대 및 회식비는 안전보건관리비로 인정되지 않습니다.
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </section>

            </div>
        </div>
    </main>

    <!-- Custom Notification Toast -->
    <div id="toast" class="fixed bottom-6 right-6 transform translate-y-20 opacity-0 transition-all duration-300 ease-out z-50 pointer-events-none">
        <div class="bg-slate-900 text-white px-5 py-3 rounded-xl shadow-2xl flex items-center border border-slate-700 text-xs">
            <i class="fa-solid fa-circle-info text-blue-400 text-sm mr-2.5" id="toastIcon"></i>
            <span id="toastMessage" class="font-medium">알림 메시지</span>
        </div>
    </div>

    <!-- Application Script -->
    <script>
        let counter = 3;
        let uploadedPhotoName = "";

        // Ministry of Employment and Labor (고용노동부 고시 제7조) Rules Engine
        const rules = [
            { 
                keywords: ['비계', '발판', '사다리', '우마', '시스템비계', '강관비계'], 
                status: '부적합', 
                reason: '<strong class="text-rose-700">제7조 제2항 (시공성 가설시설물)</strong> - 통로 및 작업발판 역할을 하는 비계·가설구조물은 직접공사비에 반영되어야 하며, 산안비로 정산 시 100% 환수 대상입니다.' 
            },
            { 
                keywords: ['신호수', '교통신호수', '신호원', '유도수', '차량유도'], 
                status: '부적합', 
                reason: '<strong class="text-rose-700">건진법 안전관리비 소관 (산안비 불인정)</strong> - 도로 점용 및 토사 운반 차량 유도를 위한 교통 신호수는 건설기술진흥법 안전관리비 항목으로 처리해야 합니다.' 
            },
            { 
                keywords: ['회식', '식대', '간식', '휴가비', '명절', '선물', '기념품', '유흥'], 
                status: '부적합', 
                reason: '<strong class="text-rose-700">제7조 제2항 (복리후생 목적 불가)</strong> - 근로자 사기진작, 복리후생, 관례적 행사를 위한 식대 및 물품은 산안비 지출 목적에 부합하지 않습니다.' 
            },
            { 
                keywords: ['과태료', '벌금', '범칙금', '지연이자', '소송'], 
                status: '부적합', 
                reason: '<strong class="text-rose-700">제7조 제2항 (벌칙성 비용 불가)</strong> - 관계 법령 위반에 따른 벌금, 과태료 등은 안전보건관리비로 계상할 수 없습니다.' 
            },
            { 
                keywords: ['cctv', 'ai', '스마트', '웨어러블', '가스감지기', '지능형'], 
                status: '조건부', 
                reason: '<strong class="text-blue-700">제7조 제1항 제2호의2 (스마트 안전장비)</strong> - 적격 품목이나 총 산안비 예산의 20% 한도 이내여야 하며, 관제화면 및 통신 연동 증빙이 필수입니다.' 
            },
            { 
                keywords: ['휴게실', '제빙기', '포도당', '아이스조끼', '쿨토시', '폭염', '한파', '핫팩'], 
                status: '조건부', 
                reason: '<strong class="text-purple-700">제7조 제1항 제6호 (근로자 건강장해 예방)</strong> - 폭염·한파 대비용품 및 자율개선 품목은 총 산안비의 15% 한도 내에서 인정됩니다. (노사협의체 의결 필요)' 
            },
            { 
                keywords: ['안전모', '안전화', '안전대', '보안경', '방진마스크', '귀마개', 'kcs', '용접장갑', '보호구', '삼각대'], 
                status: '적합', 
                reason: '<strong class="text-emerald-700">제7조 제1항 제3호 (개인보호구 및 안전장구)</strong> - KCs 안전인증을 취득한 법정 개인보호구 및 구조장비로 산안비 사용이 전액 인정됩니다.' 
            },
            { 
                keywords: ['안전관리자', '전담', '인건비', '수당'], 
                status: '적합', 
                reason: '<strong class="text-emerald-700">제7조 제1항 제1호 (인건비 및 수당)</strong> - 고용노동부 선임 신고를 필한 전담 안전관리자의 급여 및 제수당으로 적합합니다.' 
            },
            { 
                keywords: ['안전난간', '추락방지망', '낙하물방지망', '개구부덮개', '안전망'], 
                status: '적합', 
                reason: '<strong class="text-emerald-700">제7조 제1항 제2호 (안전시설비)</strong> - 추락, 낙하, 붕괴 방지를 목적으로 설치하는 순수 안전시설물이므로 적격합니다.' 
            }
        ];

        function handleKeyPress(e) {
            if (e.key === 'Enter') analyzeInput();
        }

        function setSample(text) {
            document.getElementById('expenseItem').value = text;
            analyzeInput();
        }

        function triggerFileSelect() {
            document.getElementById('fileUpload').click();
        }

        function handleFileChange(e) {
            if (e.target.files.length > 0) {
                uploadedPhotoName = e.target.files[0].name;
                document.getElementById('uploadBtnLabel').innerText = uploadedPhotoName.substring(0, 7) + '...';
                showToast(`증빙 사진 '${uploadedPhotoName}'이 첨부되었습니다.`);
            }
        }

        function showToast(message) {
            const toast = document.getElementById('toast');
            document.getElementById('toastMessage').innerText = message;
            toast.classList.remove('translate-y-20', 'opacity-0');
            setTimeout(() => {
                toast.classList.add('translate-y-20', 'opacity-0');
            }, 3000);
        }

        function analyzeExpense(itemName) {
            const normalizedInput = itemName.replace(/\s+/g, '').toLowerCase();
            
            for (let rule of rules) {
                for (let keyword of rule.keywords) {
                    if (normalizedInput.includes(keyword.toLowerCase())) {
                        return { status: rule.status, reason: rule.reason };
                    }
                }
            }
            return { 
                status: '조건부', 
                reason: '<strong class="text-slate-700">고시 세부기준 확인 필요</strong> - 명확한 8대 항목 확인이 필요합니다. 작업 안전 관련성 및 세금계산서 증빙을 검토하세요.' 
            };
        }

        function analyzeInput() {
            const inputEl = document.getElementById('expenseItem');
            const itemName = inputEl.value.trim();

            if (!itemName) {
                showToast("검토할 청구 품목을 입력해주세요.");
                inputEl.focus();
                return;
            }

            const result = analyzeExpense(itemName);
            addResultToTable(itemName, result.status, result.reason, uploadedPhotoName);
            
            inputEl.value = '';
            uploadedPhotoName = "";
            document.getElementById('uploadBtnLabel').innerText = "증빙 사진";
            showToast(`'${itemName}' AI 검토 판정 완료`);
        }

        function addResultToTable(itemName, status, reason, photo) {
            const tbody = document.getElementById('resultTableBody');
            const now = new Date();
            const dateStr = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')} ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;

            let badgeHtml = '';
            if (status === '적합') {
                badgeHtml = `
                    <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-200 status-badge">
                        <i class="fa-solid fa-circle-check mr-1 text-emerald-600"></i> 적합
                    </span>`;
            } else if (status === '부적합') {
                badgeHtml = `
                    <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-rose-100 text-rose-800 border border-rose-200 status-badge">
                        <i class="fa-solid fa-circle-xmark mr-1 text-rose-600"></i> 부적합
                    </span>`;
            } else {
                badgeHtml = `
                    <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-800 border border-amber-200 status-badge">
                        <i class="fa-solid fa-triangle-exclamation mr-1 text-amber-600"></i> 조건부
                    </span>`;
            }

            const tr = document.createElement('tr');
            tr.className = 'hover:bg-slate-50 transition';
            tr.setAttribute('data-status', status);

            tr.innerHTML = `
                <td class="px-6 py-4 text-slate-500 whitespace-nowrap">${dateStr}</td>
                <td class="px-6 py-4 font-bold text-slate-900">
                    ${escapeHtml(itemName)}
                    ${photo ? `<div class="text-[11px] font-normal text-blue-600 mt-0.5"><i class="fa-solid fa-paperclip mr-1"></i>증빙: ${escapeHtml(photo)}</div>` : ''}
                </td>
                <td class="px-6 py-4 text-center whitespace-nowrap">
                    ${badgeHtml}
                </td>
                <td class="px-6 py-4 text-slate-600 leading-relaxed">
                    ${reason}
                </td>
            `;

            tbody.insertBefore(tr, tbody.firstChild);
            counter++;
            document.getElementById('itemCount').innerText = counter;
        }

        function filterTable(status) {
            document.querySelectorAll('.filter-btn').forEach(btn => {
                if (btn.getAttribute('data-filter') === status) {
                    btn.className = "px-2.5 py-1 bg-slate-900 text-white rounded-lg font-bold filter-btn";
                } else {
                    btn.className = "px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg font-medium filter-btn";
                }
            });

            const rows = document.querySelectorAll('#resultTableBody tr');
            rows.forEach(row => {
                const rowStatus = row.getAttribute('data-status');
                if (status === '전체' || rowStatus === status) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        }

        function quickFilter(status) {
            filterTable(status);
        }

        function exportCSV() {
            let csv = "\uFEFF요청일시,청구품목,판정결과,검토근거\n";
            const rows = document.querySelectorAll('#resultTableBody tr');
            rows.forEach(r => {
                const cols = r.querySelectorAll('td');
                if (cols.length >= 4) {
                    const date = cols[0].innerText.trim();
                    const item = cols[1].innerText.replace(/\n/g, ' ').trim();
                    const status = cols[2].innerText.trim();
                    const reason = cols[3].innerText.replace(/"/g, '""').trim();
                    csv += `"${date}","${item}","${status}","${reason}"\n`;
                }
            });

            const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `산안비_AI검토결과_${new Date().toISOString().slice(0,10)}.csv`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            showToast("CSV 파일이 다운로드되었습니다.");
        }

        function escapeHtml(unsafe) {
            return unsafe
                 .replace(/&/g, "&amp;")
                 .replace(/</g, "&lt;")
                 .replace(/>/g, "&gt;")
                 .replace(/"/g, "&quot;")
                 .replace(/'/g, "&#039;");
        }
    </script>
</body>
</html>