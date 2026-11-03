<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>산업안전보건관리비 AI 검토 대시보드</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f3f4f6; /* Tailwind gray-100 */
        }
        
        /* Custom scrollbar for table */
        .table-container::-webkit-scrollbar {
            height: 8px;
            width: 8px;
        }
        .table-container::-webkit-scrollbar-track {
            background: #f1f1f1; 
            border-radius: 4px;
        }
        .table-container::-webkit-scrollbar-thumb {
            background: #c1c1c1; 
            border-radius: 4px;
        }
        .table-container::-webkit-scrollbar-thumb:hover {
            background: #a8a8a8; 
        }

        .status-badge {
            transition: all 0.3s ease;
        }
    </style>
</head>
<body class="text-gray-800 antialiased flex h-screen overflow-hidden">

    <!-- Sidebar -->
    <aside class="w-64 bg-slate-900 text-white flex-shrink-0 hidden md:flex flex-col">
        <div class="h-16 flex items-center px-6 border-b border-slate-700">
            <svg class="w-6 h-6 text-blue-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
            </svg>
            <span class="text-lg font-bold tracking-wider">SafeAI-Check</span>
        </div>
        <nav class="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
            <a href="#" class="flex items-center px-4 py-3 bg-blue-600 text-white rounded-lg">
                <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>
                검토 대시보드
            </a>
            <a href="#" class="flex items-center px-4 py-3 text-slate-300 hover:bg-slate-800 hover:text-white rounded-lg transition-colors">
                <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                검토 이력 조회
            </a>
            <a href="#" class="flex items-center px-4 py-3 text-slate-300 hover:bg-slate-800 hover:text-white rounded-lg transition-colors">
                <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"></path></svg>
                판단 기준 설정
            </a>
        </nav>
        <div class="p-4 border-t border-slate-700">
            <div class="flex items-center">
                <div class="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white font-bold">A</div>
                <div class="ml-3 text-sm">
                    <p class="font-medium text-white">안전관리자</p>
                    <p class="text-slate-400">admin@safe.ai</p>
                </div>
            </div>
        </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 flex flex-col h-full relative">
        
        <!-- Header -->
        <header class="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6 flex-shrink-0 shadow-sm z-10">
            <div class="flex items-center">
                <button class="md:hidden text-gray-500 hover:text-gray-700 focus:outline-none p-2 mr-2">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
                </button>
                <h1 class="text-xl font-semibold text-gray-800">산업안전보건관리비 AI 자동 검토</h1>
            </div>
            <div class="flex items-center space-x-4">
                <button class="text-gray-400 hover:text-gray-600 transition">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>
                </button>
            </div>
        </header>

        <!-- Content Body -->
        <div class="flex-1 overflow-y-auto p-4 md:p-6 bg-gray-50">
            
            <div class="max-w-6xl mx-auto space-y-6">
                
                <!-- Input Section -->
                <section class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
                    <div class="px-6 py-4 border-b border-gray-100 bg-gray-50/50">
                        <h2 class="text-lg font-semibold text-gray-800 flex items-center">
                            <svg class="w-5 h-5 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path></svg>
                            청구 품목 분석 (AI)
                        </h2>
                    </div>
                    <div class="p-6">
                        <div class="flex flex-col md:flex-row gap-4 items-start md:items-end">
                            <div class="flex-1 w-full">
                                <label for="expenseItem" class="block text-sm font-medium text-gray-700 mb-1">구매/집행 품목 내역 입력</label>
                                <div class="relative">
                                    <input type="text" id="expenseItem" class="block w-full pl-4 pr-12 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition shadow-sm text-gray-900" placeholder="예: KCs 인증 구조용 삼각대, 안전모, 회식비, 과태료 등 입력" onkeypress="handleKeyPress(event)">
                                    <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none text-gray-400">
                                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="flex gap-2 w-full md:w-auto">
                                <button onclick="triggerFileSelect()" class="flex-1 md:flex-none flex items-center justify-center px-4 py-3 bg-white border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-200 transition shadow-sm font-medium">
                                    <svg class="w-5 h-5 mr-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13"></path></svg>
                                    증빙 업로드
                                </button>
                                <input type="file" id="fileUpload" class="hidden">
                                
                                <button onclick="analyzeInput()" class="flex-1 md:flex-none flex items-center justify-center px-6 py-3 bg-blue-600 border border-transparent rounded-lg text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition shadow-sm font-medium">
                                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                                    AI 검토
                                </button>
                            </div>
                        </div>
                        <p class="text-xs text-gray-500 mt-3">※ 노동부 고시 '건설업 산업안전보건관리비 계상 및 사용기준' 알고리즘에 기반하여 분석됩니다.</p>
                    </div>
                </section>

                <!-- Results Section -->
                <section class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden flex flex-col">
                    <div class="px-6 py-4 border-b border-gray-100 bg-gray-50/50 flex justify-between items-center">
                        <h2 class="text-lg font-semibold text-gray-800">검토 결과 내역</h2>
                        <span class="text-xs font-medium px-2.5 py-1 bg-green-100 text-green-800 rounded-full border border-green-200">Total: <span id="itemCount">2</span>건</span>
                    </div>
                    
                    <div class="table-container overflow-x-auto w-full">
                        <table class="w-full text-left border-collapse">
                            <thead>
                                <tr class="bg-gray-50 text-gray-500 text-sm uppercase tracking-wider border-b border-gray-200">
                                    <th class="px-6 py-4 font-medium">요청일시</th>
                                    <th class="px-6 py-4 font-medium">청구 품목 / 내역</th>
                                    <th class="px-6 py-4 font-medium text-center">판정 결과</th>
                                    <th class="px-6 py-4 font-medium">AI 검토 근거 (고용노동부 기준)</th>
                                </tr>
                            </thead>
                            <tbody id="resultTableBody" class="divide-y divide-gray-100 text-sm">
                                <!-- Initial Data -->
                                <tr class="hover:bg-gray-50 transition">
                                    <td class="px-6 py-4 text-gray-500 whitespace-nowrap">2026-11-03 09:15</td>
                                    <td class="px-6 py-4 font-medium text-gray-900">KCs 인증 구조용 삼각대</td>
                                    <td class="px-6 py-4 text-center">
                                        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 border border-blue-200 status-badge">
                                            <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>
                                            적합
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 text-gray-600 line-clamp-2" title="제7조 제1항 제3호(개인보호구 및 안전장구 구입비 등). 추락방지 및 구조용 장비는 근로자 보호를 위해 사용 가능합니다.">
                                        <span class="font-semibold text-gray-700">제7조 제1항 제3호</span> - 개인보호구 및 안전장구 구입비. 추락방지 및 구조용 장비는 근로자 보호를 위해 사용 가능합니다.
                                    </td>
                                </tr>
                                <tr class="hover:bg-gray-50 transition">
                                    <td class="px-6 py-4 text-gray-500 whitespace-nowrap">2026-11-03 08:30</td>
                                    <td class="px-6 py-4 font-medium text-gray-900">현장 작업팀 안전기원 회식비</td>
                                    <td class="px-6 py-4 text-center">
                                        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800 border border-red-200 status-badge">
                                            <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                                            부적합
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 text-gray-600 line-clamp-2" title="제7조 제2항(사용불가 내역). 근로자 사기진작, 복리후생 목적의 회식비는 안전보건관리비로 계상할 수 없습니다.">
                                        <span class="font-semibold text-gray-700">사용불가(복리후생)</span> - 근로자 사기진작, 복리후생 목적의 회식비는 안전보건관리비로 계상할 수 없습니다.
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </section>

            </div>
        </div>
    </main>

    <!-- Custom Notification Toast (Instead of alert) -->
    <div id="toast" class="fixed bottom-5 right-5 transform translate-y-20 opacity-0 transition-all duration-300 ease-in-out z-50">
        <div class="bg-gray-800 text-white px-6 py-3 rounded-lg shadow-lg flex items-center">
            <svg class="w-5 h-5 mr-3 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            <span id="toastMessage">알림 메시지</span>
        </div>
    </div>

    <script>
        let counter = 2; // For initial 2 items

        // Mock AI Logic Dictionary
        const rules = [
            { keywords: ['안전모', '안전화', '안전대', '보안경', '방진마스크', 'KCs', '삼각대', '구명조끼', '개인보호구'], status: '적합', reason: '<span class="font-semibold text-gray-700">제7조 제1항 제3호</span> - 개인보호구 및 안전장구 구입비. 작업자 직접 보호를 위한 법정 보호구는 적합합니다.' },
            { keywords: ['신호수', '안전보조원', '유도자', '안전관리자', '인건비'], status: '적합', reason: '<span class="font-semibold text-gray-700">제7조 제1항 제1호</span> - 안전관리자 등의 인건비. 전담 안전관리자 및 안전보조 작업자의 인건비로 사용 가능합니다.' },
            { keywords: ['위험성평가', '컨설팅', '안전보건진단', '측정'], status: '적합', reason: '<span class="font-semibold text-gray-700">제7조 제1항 제4호</span> - 사업장의 안전보건진단, 작업환경측정 등 재해예방을 위한 기술지도 및 자문 비용으로 적합합니다.' },
            { keywords: ['회식', '간식', '휴가비', '명절', '선물', '복리후생'], status: '부적합', reason: '<span class="font-semibold text-gray-700">사용불가 내역</span> - 근로자 사기진작, 복리후생 목적의 비용은 안전보건관리비 목적에 부합하지 않습니다.' },
            { keywords: ['벌금', '과태료', '범칙금', '지연이자'], status: '부적합', reason: '<span class="font-semibold text-gray-700">사용불가 내역</span> - 법령 위반에 따른 제재금 성격의 비용은 안전재해예방 목적이 아니므로 불가합니다.' },
            { keywords: ['사무용품', '프린터', 'A4', '일반가구', '책상'], status: '부적합', reason: '<span class="font-semibold text-gray-700">사용불가 내역</span> - 현장 안전관리와 직접적인 관련이 없는 일반 사무용품 구입비는 불가합니다.' },
            { keywords: ['휴게실', '에어컨', '난로', '제빙기', '폭염', '한파'], status: '부분적합', reason: '<span class="font-semibold text-gray-700">제7조 제1항 제6호 (조건부)</span> - 폭염/한파 등 기후변화에 따른 건강장해 예방 목적의 설비(제빙기, 핫팩 등)는 사용 가능하나, 일반 휴게시설 설치비는 별도 확인이 필요합니다.' },
        ];

        function handleKeyPress(e) {
            if (e.key === 'Enter') {
                analyzeInput();
            }
        }

        function triggerFileSelect() {
            document.getElementById('fileUpload').click();
        }

        // Handle file selection (UI simulation)
        document.getElementById('fileUpload').addEventListener('change', function(e) {
            if(e.target.files.length > 0) {
                showToast(`'${e.target.files[0].name}' 파일이 업로드 되었습니다. (디자인용)`);
            }
        });

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
                status: '검토필요', 
                reason: '<span class="font-semibold text-yellow-700">추가 확인 요망</span> - 해당 품목은 자동 분류 키워드에 해당하지 않습니다. 작업과의 직접적인 연관성 및 세부 규정(고시) 확인이 필요합니다.' 
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

            // Simulate processing delay for AI feel
            const btn = document.querySelector('button[onclick="analyzeInput()"]');
            const originalBtnContent = btn.innerHTML;
            btn.innerHTML = `<svg class="animate-spin h-5 w-5 mr-2 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> 분석 중...`;
            btn.disabled = true;
            inputEl.disabled = true;

            setTimeout(() => {
                const result = analyzeExpense(itemName);
                addResultToTable(itemName, result.status, result.reason);
                
                inputEl.value = '';
                btn.innerHTML = originalBtnContent;
                btn.disabled = false;
                inputEl.disabled = false;
                inputEl.focus();
                showToast("AI 검토가 완료되었습니다.");
                
            }, 800); // 0.8s fake delay
        }

        function addResultToTable(itemName, status, reason) {
            const tbody = document.getElementById('resultTableBody');
            
            // Format current date/time
            const now = new Date();
            const dateStr = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')} ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;

            // Define badge styling based on status
            let badgeClass, iconSvg;
            if (status === '적합') {
                badgeClass = 'bg-blue-100 text-blue-800 border-blue-200';
                iconSvg = `<svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>`;
            } else if (status === '부적합') {
                badgeClass = 'bg-red-100 text-red-800 border-red-200';
                iconSvg = `<svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>`;
            } else { // 부분적합, 검토필요 등
                badgeClass = 'bg-yellow-100 text-yellow-800 border-yellow-200';
                iconSvg = `<svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>`;
            }

            const tr = document.createElement('tr');
            tr.className = 'hover:bg-gray-50 transition opacity-0';
            
            // Extract raw text for title attribute tooltip
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = reason;
            const plainReason = tempDiv.textContent || tempDiv.innerText || "";

            tr.innerHTML = `
                <td class="px-6 py-4 text-gray-500 whitespace-nowrap">${dateStr}</td>
                <td class="px-6 py-4 font-medium text-gray-900">${escapeHtml(itemName)}</td>
                <td class="px-6 py-4 text-center">
                    <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border ${badgeClass} status-badge">
                        ${iconSvg}
                        ${status}
                    </span>
                </td>
                <td class="px-6 py-4 text-gray-600 line-clamp-2" title="${escapeHtml(plainReason)}">
                    ${reason}
                </td>
            `;

            tbody.insertBefore(tr, tbody.firstChild);
            
            // Trigger animation
            setTimeout(() => {
                tr.classList.remove('opacity-0');
            }, 50);

            // Update counter
            counter++;
            document.getElementById('itemCount').innerText = counter;
        }

        // Basic HTML entity escape for security
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