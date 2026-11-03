<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 산안비 사용내역서 및 증빙 사진 대조 검토 시스템</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        navy: { 800: '#1e293b', 900: '#0f172a' },
                        safeblue: '#1d4ed8',
                        safeamber: '#d97706',
                        safegreen: '#059669',
                        safered: '#dc2626'
                    }
                }
            }
        }
    </script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Pretendard', sans-serif; }
        .custom-scrollbar::-webkit-scrollbar { width: 6px; height: 6px; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
        @media print {
            .no-print { display: none !important; }
            .print-full { width: 100% !important; margin: 0 !important; }
        }
    </style>
</head>
<body class="bg-slate-100 text-slate-800 min-h-screen flex flex-col antialiased">

    <!-- Top Navigation Header -->
    <header class="bg-slate-900 text-white shadow-lg border-b border-slate-800 sticky top-0 z-30 no-print">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="bg-blue-600 p-2.5 rounded-xl text-white flex items-center justify-center shadow-lg shadow-blue-500/30">
                    <i class="fa-solid fa-shield-halved text-xl"></i>
                </div>
                <div>
                    <h1 class="text-base sm:text-lg font-bold tracking-tight text-white flex items-center gap-2">
                        AI 산안비 사용내역 및 현장 증빙 대조 검토기
                        <span class="text-[11px] font-semibold bg-emerald-950 text-emerald-300 border border-emerald-700/60 px-2 py-0.5 rounded-md">고용노동부 고시 제2023-49호</span>
                    </h1>
                    <p class="text-xs text-slate-400 hidden sm:block">지출 품목 8대 항목 분류 및 설치 전·후 사진/인증마크 AI 크로스체크</p>
                </div>
            </div>
            <div class="flex items-center gap-2">
                <button onclick="loadRealisticPreset()" class="text-xs bg-blue-600/20 hover:bg-blue-600/30 text-blue-300 border border-blue-500/40 px-3 py-1.5 rounded-lg transition flex items-center gap-1.5 font-medium">
                    <i class="fa-solid fa-wand-magic-sparkles"></i> 실무 예시 일괄 로드
                </button>
                <button onclick="window.print()" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 px-3 py-1.5 rounded-lg transition flex items-center gap-1.5">
                    <i class="fa-solid fa-print"></i> 보고서 인쇄
                </button>
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <main class="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8 space-y-6">

        <!-- Budget & Legal Quota Indicator Cards -->
        <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 no-print">
            <!-- Total Budget Card -->
            <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm relative overflow-hidden">
                <div class="flex items-center justify-between text-xs text-slate-500 font-medium">
                    <span>총 산안비 계상 예산</span>
                    <button onclick="openBudgetModal()" class="text-blue-600 hover:text-blue-800 text-xs font-semibold">설정 변경</button>
                </div>
                <div class="mt-2 flex items-baseline justify-between">
                    <span class="text-2xl font-black text-slate-900" id="totalBudgetDisplay">₩ 100,000,000</span>
                </div>
                <div class="mt-3 pt-3 border-t border-slate-100 flex justify-between text-xs text-slate-500">
                    <span>정산 인정 누적</span>
                    <span class="font-bold text-slate-700" id="statApprovedAmount">₩ 0</span>
                </div>
            </div>

            <!-- Execution Status -->
            <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm">
                <div class="flex items-center justify-between text-xs text-slate-500 font-medium">
                    <span>전체 예산 집행률</span>
                    <span id="execRateBadge" class="text-xs px-2 py-0.5 rounded-md bg-slate-100 text-slate-600 font-bold">0.0%</span>
                </div>
                <div class="mt-2 text-2xl font-black text-slate-900" id="statRemainingBudget">₩ 100,000,000</div>
                <div class="w-full bg-slate-100 rounded-full h-2 mt-3 overflow-hidden">
                    <div id="execProgressBar" class="bg-emerald-500 h-2 rounded-full transition-all duration-500" style="width: 0%"></div>
                </div>
            </div>

            <!-- Smart Tech Limit (20%) -->
            <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm">
                <div class="flex items-center justify-between text-xs text-slate-500 font-medium">
                    <span class="flex items-center gap-1.5"><i class="fa-solid fa-microchip text-blue-600"></i> 스마트 안전장비 (20%)</span>
                    <span id="smartStatusBadge" class="text-[11px] font-bold px-2 py-0.5 rounded bg-blue-50 text-blue-700">적정</span>
                </div>
                <div class="mt-2 flex items-baseline justify-between">
                    <span class="text-xl font-extrabold text-blue-900" id="smartUsedDisplay">₩ 0</span>
                    <span class="text-xs text-slate-400" id="smartLimitDisplay">한도 ₩ 20,000,000</span>
                </div>
                <div class="w-full bg-slate-100 rounded-full h-2 mt-3 overflow-hidden">
                    <div id="smartProgressBar" class="bg-blue-600 h-2 rounded-full transition-all" style="width: 0%"></div>
                </div>
            </div>

            <!-- Worker Autonomous Limit (15%) -->
            <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm">
                <div class="flex items-center justify-between text-xs text-slate-500 font-medium">
                    <span class="flex items-center gap-1.5"><i class="fa-solid fa-users text-purple-600"></i> 자율개선 품목 (15%)</span>
                    <span id="workerStatusBadge" class="text-[11px] font-bold px-2 py-0.5 rounded bg-purple-50 text-purple-700">적정</span>
                </div>
                <div class="mt-2 flex items-baseline justify-between">
                    <span class="text-xl font-extrabold text-purple-900" id="workerUsedDisplay">₩ 0</span>
                    <span class="text-xs text-slate-400" id="workerLimitDisplay">한도 ₩ 15,000,000</span>
                </div>
                <div class="w-full bg-slate-100 rounded-full h-2 mt-3 overflow-hidden">
                    <div id="workerProgressBar" class="bg-purple-600 h-2 rounded-full transition-all" style="width: 0%"></div>
                </div>
            </div>
        </section>

        <!-- Twin Input/Upload Area: 1) Usage Details + 2) Evidence Photos -->
        <section class="grid grid-cols-1 lg:grid-cols-2 gap-6 no-print">

            <!-- Card 1: Usage Details Input (Excel/CSV or Form) -->
            <div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-5 flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between pb-3 border-b border-slate-100 mb-4">
                        <div class="flex items-center gap-2">
                            <span class="w-7 h-7 rounded-lg bg-blue-100 text-blue-700 flex items-center justify-center font-black text-sm">1</span>
                            <h2 class="font-bold text-slate-900 text-sm sm:text-base">사용내역서 등록 (지출 내역)</h2>
                        </div>
                        <button onclick="toggleInputMode()" id="modeToggleBtn" class="text-xs text-blue-600 hover:text-blue-800 font-medium flex items-center gap-1">
                            <i class="fa-solid fa-file-excel"></i> 엑셀/텍스트 붙여넣기 모드
                        </button>
                    </div>

                    <!-- Direct Form Input Mode -->
                    <form id="itemDirectForm" onsubmit="event.preventDefault(); submitItemFromForm();" class="space-y-3">
                        <div>
                            <label class="block text-xs font-bold text-slate-700 mb-1">품목명 <span class="text-red-500">*</span></label>
                            <input type="text" id="formItemName" required placeholder="예: 용접용 안전장갑, 시스템 비계, 이동형 AI CCTV" 
                                   class="w-full text-xs sm:text-sm px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none">
                        </div>

                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="block text-xs font-bold text-slate-700 mb-1">지출 신청 금액 (원) <span class="text-red-500">*</span></label>
                                <input type="number" id="formItemAmount" required min="100" placeholder="금액 입력" 
                                       class="w-full text-xs sm:text-sm px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none">
                            </div>
                            <div>
                                <label class="block text-xs font-bold text-slate-700 mb-1">청구 법정 항목 (1~8호)</label>
                                <select id="formItemCategory" class="w-full text-xs sm:text-sm px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none">
                                    <option value="1">1호. 안전관리자 인건비/수당</option>
                                    <option value="2">2호. 안전시설비 등</option>
                                    <option value="3" selected>3호. 개인보호구 및 안전장구</option>
                                    <option value="4">4호. 사업장 안전보건진단비</option>
                                    <option value="5">5호. 안전보건교육비 및 행사비</option>
                                    <option value="6">6호. 근로자 건강관리비 등</option>
                                    <option value="7">7호. 재해예방 기술지도비</option>
                                    <option value="8">8호. 본사 전담조직 운영비</option>
                                </select>
                            </div>
                        </div>

                        <div>
                            <label class="block text-xs font-bold text-slate-700 mb-1">현장 설치/사용 목적 및 장소 상세</label>
                            <textarea id="formItemUsage" rows="2" placeholder="예: 지하층 굴착 구간 질식 위험 모니터링 또는 고소 작업자 추락 방지용" 
                                      class="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none custom-scrollbar"></textarea>
                        </div>

                        <div class="bg-slate-50 p-2.5 rounded-lg border border-slate-200 grid grid-cols-2 gap-2 text-xs">
                            <label class="flex items-center gap-2 cursor-pointer">
                                <input type="checkbox" id="formIsSmart" class="rounded text-blue-600 focus:ring-blue-500">
                                <span class="text-slate-700 font-medium">스마트 안전장비 (20%)</span>
                            </label>
                            <label class="flex items-center gap-2 cursor-pointer">
                                <input type="checkbox" id="formIsWorker" class="rounded text-purple-600 focus:ring-purple-500">
                                <span class="text-slate-700 font-medium">노사 자율개선 (15%)</span>
                            </label>
                        </div>

                        <button type="submit" class="w-full bg-slate-900 hover:bg-slate-800 text-white font-bold py-2 rounded-lg text-xs transition flex items-center justify-center gap-1.5">
                            <i class="fa-solid fa-plus"></i> 사용내역에 추가
                        </button>
                    </form>

                    <!-- Batch / CSV Paste Mode (Hidden initially) -->
                    <div id="batchPasteMode" class="hidden space-y-3">
                        <p class="text-xs text-slate-500">엑셀 열(품목명, 금액, 용도)을 복사해서 붙여넣거나 CSV 형식 텍스트를 입력하세요.</p>
                        <textarea id="csvBatchInput" rows="6" placeholder="용접장갑, 450000, 3호 보호구 지급
시스템 비계, 12000000, 외부 도장용 비계 설치
이동형 AI CCTV, 5000000, 스마트 추락 감시 모니터링" 
                                  class="w-full text-xs font-mono p-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"></textarea>
                        <button onclick="parseBatchInput()" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 rounded-lg text-xs transition flex items-center justify-center gap-1.5">
                            <i class="fa-solid fa-file-import"></i> 텍스트 내역 일괄 파싱 및 등록
                        </button>
                    </div>
                </div>
            </div>

            <!-- Card 2: Field Evidence Photos & Files Upload -->
            <div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-5 flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between pb-3 border-b border-slate-100 mb-4">
                        <div class="flex items-center gap-2">
                            <span class="w-7 h-7 rounded-lg bg-teal-100 text-teal-700 flex items-center justify-center font-black text-sm">2</span>
                            <h2 class="font-bold text-slate-900 text-sm sm:text-base">현장 증빙 사진 및 서류 업로드</h2>
                        </div>
                        <span class="text-xs text-slate-400" id="photoCountDisplay">등록된 증빙: 0건</span>
                    </div>

                    <!-- Dropzone -->
                    <div id="photoDropzone" onclick="document.getElementById('photoFileInput').click()"
                         class="border-2 border-dashed border-slate-300 hover:border-blue-500 bg-slate-50 hover:bg-blue-50/40 rounded-xl p-5 text-center cursor-pointer transition flex flex-col items-center justify-center space-y-2">
                        <i class="fa-solid fa-cloud-arrow-up text-3xl text-slate-400"></i>
                        <div class="text-xs font-bold text-slate-700">현장 설치 전/후 사진, 송장, KCs 인증표 드래그 또는 클릭</div>
                        <p class="text-[11px] text-slate-400">JPG, PNG, WebP 지원 (다중 파일 업로드 가능)</p>
                        <input type="file" id="photoFileInput" multiple accept="image/*" class="hidden" onchange="handlePhotoUpload(this.files)">
                    </div>

                    <!-- Evidence Preview Grid -->
                    <div class="mt-4">
                        <div class="text-xs font-bold text-slate-700 mb-2 flex items-center justify-between">
                            <span>업로드된 증빙 사진 갤러리</span>
                            <span class="text-[11px] text-slate-400">클릭 시 확대 및 태그 확인</span>
                        </div>
                        <div id="evidenceGallery" class="grid grid-cols-3 sm:grid-cols-4 gap-2.5 max-h-48 overflow-y-auto custom-scrollbar p-1">
                            <div class="col-span-full text-center py-6 text-xs text-slate-400">
                                아직 업로드된 사진이 없습니다. 위 박스에 사진을 추가하세요.
                            </div>
                        </div>
                    </div>
                </div>

                <div class="pt-4 border-t border-slate-100 mt-4 flex items-center justify-between">
                    <button onclick="clearAllPhotos()" class="text-xs text-slate-500 hover:text-red-600 transition flex items-center gap-1">
                        <i class="fa-solid fa-trash-can"></i> 사진 전체 비우기
                    </button>
                    <button onclick="runAIAudit()" class="bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2.5 px-6 rounded-xl text-xs sm:text-sm shadow-md shadow-emerald-600/30 transition flex items-center gap-2">
                        <i class="fa-solid fa-magnifying-glass-chart"></i> AI 종합 대조 검토 실행
                    </button>
                </div>
            </div>

        </section>

        <!-- AI Audit Analysis Summary Banner -->
        <section id="auditSummaryBanner" class="bg-gradient-to-r from-slate-900 to-blue-950 text-white p-5 rounded-2xl shadow-md border border-slate-800 hidden">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <span class="text-xs font-bold text-blue-400 uppercase tracking-wider flex items-center gap-1.5">
                        <i class="fa-solid fa-microchip"></i> AI 고용노동부 고시 대조 검토 보고서
                    </span>
                    <h3 class="text-lg font-black text-white mt-1" id="auditSummaryHeading">총 4건 중 2건 적격, 1건 부적격, 1건 보완필요</h3>
                    <p class="text-xs text-slate-300 mt-0.5" id="auditSummaryDetail">불인정(부적격) 예상 금액: ₩ 15,200,000 (환수 위험 품목 감지됨)</p>
                </div>
                <div class="flex items-center gap-2 self-start md:self-auto">
                    <button onclick="filterAuditTable('ALL')" class="px-3 py-1.5 text-xs font-bold rounded-lg bg-white/10 hover:bg-white/20 transition">전체</button>
                    <button onclick="filterAuditTable('APPROVED')" class="px-3 py-1.5 text-xs font-bold rounded-lg bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 hover:bg-emerald-500/30 transition">적격만</button>
                    <button onclick="filterAuditTable('REJECTED')" class="px-3 py-1.5 text-xs font-bold rounded-lg bg-red-500/20 text-red-300 border border-red-500/30 hover:bg-red-500/30 transition">부적격만</button>
                    <button onclick="filterAuditTable('WARNING')" class="px-3 py-1.5 text-xs font-bold rounded-lg bg-amber-500/20 text-amber-300 border border-amber-500/30 hover:bg-amber-500/30 transition">보완필요만</button>
                </div>
            </div>
        </section>

        <!-- Detailed Audit Ledger / Card View -->
        <section class="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
                <div>
                    <h3 class="text-base font-bold text-slate-900 flex items-center gap-2">
                        <i class="fa-solid fa-clipboard-check text-blue-600"></i>
                        산안비 지출 및 증빙 대조 정산 내역서
                    </h3>
                    <p class="text-xs text-slate-500">사용내역서 품목과 업로드된 사진 증빙을 자동 매칭 분석한 세부 결과입니다.</p>
                </div>
                <div class="flex items-center gap-2 no-print">
                    <button onclick="exportAuditReportCSV()" class="text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 px-3 py-2 rounded-lg border border-slate-300 transition flex items-center gap-1.5 font-semibold">
                        <i class="fa-solid fa-file-excel text-emerald-600"></i> 검토결과 엑셀(CSV) 저장
                    </button>
                </div>
            </div>

            <!-- Audit Cards Container -->
            <div id="auditItemsContainer" class="space-y-4">
                <!-- Dynamically generated items -->
            </div>

            <!-- Empty State -->
            <div id="auditEmptyState" class="py-12 text-center text-slate-400 text-sm">
                <i class="fa-solid fa-folder-open text-4xl mb-3 text-slate-300"></i>
                <p>등록된 정산 내역이 없습니다. 좌측 상단의 <strong>[실무 예시 일괄 로드]</strong> 버튼을 누르거나 직접 입력해보세요.</p>
            </div>
        </section>

        <!-- Legal Citation & Audit Guide Footer Info -->
        <section class="bg-slate-50 rounded-2xl border border-slate-200 p-5 text-xs text-slate-600 space-y-2">
            <div class="font-bold text-slate-800 flex items-center gap-1.5">
                <i class="fa-solid fa-circle-exclamation text-blue-600"></i> 고용노동부 산안비 감독관 실사 대비 필수 체크포인트
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-3 pt-2 text-[11px] leading-relaxed">
                <div class="p-3 bg-white rounded-xl border border-slate-200">
                    <strong class="text-slate-800 block mb-1">1. 시공성 가설물 분리</strong>
                    비계, 발판, 사다리, 가설통로는 공사원가 직접비 항목입니다. 산안비로 정산 시 100% 환수 및 과태료 대상이 됩니다.
                </div>
                <div class="p-3 bg-white rounded-xl border border-slate-200">
                    <strong class="text-slate-800 block mb-1">2. 건진법 신호수 제외</strong>
                    외부 공사차량 유도 및 도로교통 신호수는 건설기술진흥법 안전관리비입니다. 산안비 적용 불가합니다.
                </div>
                <div class="p-3 bg-white rounded-xl border border-slate-200">
                    <strong class="text-slate-800 block mb-1">3. 증빙 사진 필수 태그</strong>
                    보호구는 'KCs 인증마크', 스마트장비는 '통신/모니터링 동작화면', 자율품목은 '회의록+현장사용' 사진이 구비되어야 인정됩니다.
                </div>
            </div>
        </section>

    </main>

    <!-- Modal for Image Preview & Tag Edit -->
    <div id="imageDetailModal" class="fixed inset-0 bg-slate-950/70 backdrop-blur-sm z-50 flex items-center justify-center hidden p-4">
        <div class="bg-white rounded-2xl max-w-lg w-full p-5 space-y-4 shadow-2xl">
            <div class="flex items-center justify-between border-b pb-2">
                <h4 class="font-bold text-slate-900 text-sm" id="modalImgTitle">증빙 사진 상세 정보</h4>
                <button onclick="closeImageModal()" class="text-slate-400 hover:text-slate-600"><i class="fa-solid fa-xmark text-lg"></i></button>
            </div>
            <div class="w-full h-64 bg-slate-100 rounded-xl overflow-hidden flex items-center justify-center border border-slate-200">
                <img id="modalImgElement" src="" alt="증빙 미리보기" class="max-h-full max-w-full object-contain">
            </div>
            <div class="space-y-2 text-xs">
                <div>
                    <span class="font-semibold text-slate-700">추출된 이미지 AI 태그:</span>
                    <span id="modalImgTags" class="text-blue-600 font-mono ml-1">KCs 마크, 안전모, 설치전경</span>
                </div>
                <div>
                    <span class="font-semibold text-slate-700">매칭된 사용내역서 품목:</span>
                    <span id="modalImgMatch" class="text-emerald-700 font-bold ml-1">용접용 안전장갑</span>
                </div>
            </div>
            <button onclick="closeImageModal()" class="w-full bg-slate-900 text-white font-bold py-2 rounded-xl text-xs">닫기</button>
        </div>
    </div>

    <!-- Modal for Budget Setting -->
    <div id="budgetModal" class="fixed inset-0 bg-slate-950/60 backdrop-blur-sm z-50 flex items-center justify-center hidden p-4">
        <div class="bg-white rounded-2xl max-w-md w-full p-6 space-y-4 shadow-2xl">
            <h4 class="text-base font-bold text-slate-900">도급 산안비 예산 총액 변경</h4>
            <p class="text-xs text-slate-500 leading-relaxed">
                공사 도급내역서상의 안전보건관리비 총액을 입력하세요. 스마트 안전장비(20%) 및 자율개선(15%) 한도액이 자동으로 재계산됩니다.
            </p>
            <div>
                <label class="block text-xs font-bold text-slate-700 mb-1">총 예산 (원)</label>
                <input type="number" id="inputBudgetModal" class="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm font-bold focus:ring-2 focus:ring-blue-500">
            </div>
            <div class="flex justify-end gap-2 pt-2">
                <button onclick="closeBudgetModal()" class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-semibold">취소</button>
                <button onclick="saveBudgetModal()" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-bold">저장 및 재산출</button>
            </div>
        </div>
    </div>

    <!-- In-page Message Toast -->
    <div id="toastMessage" class="fixed bottom-6 right-6 bg-slate-900 text-white px-4 py-3 rounded-xl shadow-2xl text-xs flex items-center gap-2 z-50 border border-slate-700 transition-all duration-300 transform translate-y-20 opacity-0 pointer-events-none">
        <i class="fa-solid fa-circle-check text-emerald-400 text-base" id="toastIcon"></i>
        <span id="toastText">작업이 완료되었습니다.</span>
    </div>

    <!-- Core Logic JavaScript -->
    <script>
        // System State
        let totalBudget = 100000000;
        let activeFilter = 'ALL';

        // 8 Categories Description
        const CATEGORIES = {
            1: "1호. 안전관리자 인건비/수당",
            2: "2호. 안전시설비 등",
            3: "3호. 개인보호구 및 안전장구",
            4: "4호. 사업장 안전보건진단비",
            5: "5호. 안전보건교육비 및 행사비",
            6: "6호. 근로자 건강관리비 등",
            7: "7호. 재해예방 기술지도비",
            8: "8호. 본사 전담조직 운영비"
        };

        // Evidence Photos Library
        let uploadedPhotos = [];

        // Usage Items & Audit Data
        let auditItems = [];

        // Realistic Real-world Presets (4 Cases asked by user)
        const PRESET_CASES = [
            {
                id: 101,
                name: "용접용 안전장갑 및 2급 방진마스크 (KCs 인증)",
                amount: 850000,
                category: 3,
                usage: "배관 용접 및 철골 화기작업자 대상 한국산업안전보건공단 KCs 인증 보호구 지급",
                isSmart: false,
                isWorker: false,
                // Simulated photo evidence
                photoName: "용접장갑_KCs마크_및_지급대장.jpg",
                photoUrl: "https://images.unsplash.com/photo-1578885136359-16c8bd4d3a8e?auto=format&fit=crop&w=400&q=80",
                photoTags: ["KCs안전인증", "보호구지급서명부", "용접장갑실물"],
                evidenceState: "MATCHED"
            },
            {
                id: 102,
                name: "외벽 도장용 시스템 비계 및 작업발판 임대료",
                amount: 12000000,
                category: 2,
                usage: "본동 외벽 수성페인트 도장 및 코킹 작업을 위한 외부 시스템 비계 설치",
                isSmart: false,
                isWorker: false,
                photoName: "시스템비계_설치사진.jpg",
                photoUrl: "https://images.unsplash.com/photo-1541888946425-d0fbb186f5f7?auto=format&fit=crop&w=400&q=80",
                photoTags: ["가설구조물", "외부비계", "발판"],
                evidenceState: "DISALLOWED_STRUCTURE"
            },
            {
                id: 103,
                name: "지능형 이동식 AI CCTV 관제 카메라 임대 (위험구역 추락방지)",
                amount: 6500000,
                category: 2,
                usage: "고위험 개구부 및 타워크레인 양중구역 근로자 접근 실시간 AI 감지 및 경보",
                isSmart: true,
                isWorker: false,
                photoName: "스마트_AI_CCTV_현장설치전경.jpg",
                photoUrl: "https://images.unsplash.com/photo-1557597774-9d273605dfa9?auto=format&fit=crop&w=400&q=80",
                photoTags: ["스마트안전장비", "모니터링화면", "AI감지"],
                evidenceState: "SMART_LIMIT_CHECK"
            },
            {
                id: 104,
                name: "덤프트럭 토사 반출 진입로 교통 신호수 인건비",
                amount: 3200000,
                category: 1,
                usage: "현장 정문 앞 일반 도로 점용 및 토사 운반 덤프트럭 출입 유도 교통정리",
                isSmart: false,
                isWorker: false,
                photoName: "도로교통_신호수_배치사진.jpg",
                photoUrl: "https://images.unsplash.com/photo-1508873696983-2df5293cb32f?auto=format&fit=crop&w=400&q=80",
                photoTags: ["도로교통정리", "신호봉", "덤프트럭유도"],
                evidenceState: "LAW_MISMATCH"
            }
        ];

        // Format Currency Helper
        function formatKRW(val) {
            return "₩ " + Number(val || 0).toLocaleString();
        }

        // Show Toast Notification
        function showToast(msg, isSuccess = true) {
            const toast = document.getElementById('toastMessage');
            const toastText = document.getElementById('toastText');
            const toastIcon = document.getElementById('toastIcon');

            toastText.textContent = msg;
            toastIcon.className = isSuccess 
                ? "fa-solid fa-circle-check text-emerald-400 text-base" 
                : "fa-solid fa-triangle-exclamation text-amber-400 text-base";

            toast.classList.remove('translate-y-20', 'opacity-0', 'pointer-events-none');
            setTimeout(() => {
                toast.classList.add('translate-y-20', 'opacity-0', 'pointer-events-none');
            }, 3000);
        }

        // Toggle Input Mode (Direct vs CSV Paste)
        function toggleInputMode() {
            const form = document.getElementById('itemDirectForm');
            const batch = document.getElementById('batchPasteMode');
            const btn = document.getElementById('modeToggleBtn');

            if (form.classList.contains('hidden')) {
                form.classList.remove('hidden');
                batch.classList.add('hidden');
                btn.innerHTML = '<i class="fa-solid fa-file-excel"></i> 엑셀/텍스트 붙여넣기 모드';
            } else {
                form.classList.add('hidden');
                batch.classList.remove('hidden');
                btn.innerHTML = '<i class="fa-solid fa-pen-to-square"></i> 단일 품목 직접 입력 모드';
            }
        }

        // Parse Batch CSV/Text input
        function parseBatchInput() {
            const text = document.getElementById('csvBatchInput').value.trim();
            if (!text) {
                showToast("파싱할 텍스트를 입력해주세요.", false);
                return;
            }

            const lines = text.split('\n');
            let addedCount = 0;

            lines.forEach(line => {
                const parts = line.split(/[,\t]+/).map(p => p.trim());
                if (parts.length >= 2) {
                    const name = parts[0];
                    const amount = parseInt(parts[1].replace(/[^0-9]/g, ''), 10) || 0;
                    const usage = parts[2] || "현장 안전용품 구입";
                    
                    if (name && amount > 0) {
                        auditItems.push({
                            id: Date.now() + Math.random(),
                            name,
                            amount,
                            category: 2, // 기본 2호 지정 후 AI 판단
                            usage,
                            isSmart: name.includes("스마트") || name.includes("AI") || name.includes("센서"),
                            isWorker: name.includes("휴게") || name.includes("폭염") || name.includes("아이스"),
                            photoName: null,
                            photoUrl: null,
                            photoTags: [],
                            evidenceState: "PENDING_AUDIT"
                        });
                        addedCount++;
                    }
                }
            });

            if (addedCount > 0) {
                document.getElementById('csvBatchInput').value = '';
                toggleInputMode();
                runAIAudit();
                showToast(`${addedCount}개 품목이 등록되었습니다.`);
            } else {
                showToast("올바른 형식(품목명, 금액)을 찾지 못했습니다.", false);
            }
        }

        // Add single item via Form
        function submitItemFromForm() {
            const name = document.getElementById('formItemName').value.trim();
            const amount = parseInt(document.getElementById('formItemAmount').value, 10);
            const category = parseInt(document.getElementById('formItemCategory').value, 10);
            const usage = document.getElementById('formItemUsage').value.trim();
            const isSmart = document.getElementById('formIsSmart').checked;
            const isWorker = document.getElementById('formIsWorker').checked;

            if (!name || isNaN(amount) || amount <= 0) {
                showToast("품목명과 유효한 금액을 입력해주세요.", false);
                return;
            }

            // Find matching photo from uploaded list if any
            let matchedPhoto = uploadedPhotos.find(p => !p.assigned && (name.includes(p.tagKey) || usage.includes(p.tagKey)));
            let photoUrl = null;
            let photoName = null;
            let photoTags = [];

            if (matchedPhoto) {
                matchedPhoto.assigned = true;
                photoUrl = matchedPhoto.url;
                photoName = matchedPhoto.name;
                photoTags = matchedPhoto.tags;
            }

            const newItem = {
                id: Date.now(),
                name,
                amount,
                category,
                usage: usage || "현장 안전 보건 관리 목적",
                isSmart,
                isWorker,
                photoName,
                photoUrl,
                photoTags,
                evidenceState: photoUrl ? "MATCHED" : "NO_PHOTO"
            };

            auditItems.unshift(newItem);
            document.getElementById('itemDirectForm').reset();
            runAIAudit();
            showToast("사용내역이 추가되었습니다.");
        }

        // Handle Photo Upload & Simulated AI Vision Tagging
        function handlePhotoUpload(files) {
            if (!files || files.length === 0) return;

            Array.from(files).forEach(file => {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const fileNameLower = file.name.toLowerCase();
                    
                    // Simulate AI Tagging based on filename or random safety traits
                    let tags = ["현장실물사진", "설치후"];
                    let tagKey = "";

                    if (fileNameLower.includes("비계") || fileNameLower.includes("발판")) {
                        tags = ["가설구조물", "외부비계", "발판", "시공성구조체"];
                        tagKey = "비계";
                    } else if (fileNameLower.includes("cctv") || fileNameLower.includes("ai") || fileNameLower.includes("스마트")) {
                        tags = ["스마트장비", "AI관제화면", "통신센서"];
                        tagKey = "cctv";
                    } else if (fileNameLower.includes("신호수") || fileNameLower.includes("유도원")) {
                        tags = ["도로교통정리", "신호봉", "조끼"];
                        tagKey = "신호수";
                    } else if (fileNameLower.includes("장갑") || fileNameLower.includes("보호구") || fileNameLower.includes("마스크") || fileNameLower.includes("모")) {
                        tags = ["KCs안전인증마크", "보호구지급서명부", "개인보호구"];
                        tagKey = "보호구";
                    } else {
                        tags = ["현장안전시설", "설치확인"];
                        tagKey = "안전";
                    }

                    const photoObj = {
                        id: Date.now() + Math.random(),
                        name: file.name,
                        url: e.target.result,
                        tags: tags,
                        tagKey: tagKey,
                        assigned: false
                    };

                    uploadedPhotos.push(photoObj);
                    renderPhotoGallery();
                    autoMatchPhotosToLedger();
                };
                reader.readAsDataURL(file);
            });

            showToast(`${files.length}장의 증빙 사진이 등록되었습니다.`);
        }

        // Render Photo Gallery
        function renderPhotoGallery() {
            const gallery = document.getElementById('evidenceGallery');
            document.getElementById('photoCountDisplay').innerText = `등록된 증빙: ${uploadedPhotos.length}건`;

            if (uploadedPhotos.length === 0) {
                gallery.innerHTML = `
                    <div class="col-span-full text-center py-6 text-xs text-slate-400">
                        아직 업로드된 사진이 없습니다. 위 박스에 사진을 추가하세요.
                    </div>`;
                return;
            }

            gallery.innerHTML = uploadedPhotos.map((p, idx) => `
                <div class="group relative bg-slate-100 rounded-lg overflow-hidden border border-slate-200 aspect-square cursor-pointer hover:border-blue-500 transition" onclick="openImageModal(${idx})">
                    <img src="${p.url}" alt="${p.name}" class="w-full h-full object-cover">
                    <div class="absolute inset-0 bg-slate-900/60 opacity-0 group-hover:opacity-100 transition flex flex-col justify-end p-1.5 text-white">
                        <span class="text-[9px] truncate font-medium">${p.name}</span>
                        <div class="flex flex-wrap gap-0.5 mt-0.5">
                            ${p.tags.slice(0, 2).map(t => `<span class="bg-blue-600/80 text-[8px] px-1 rounded">${t}</span>`).join('')}
                        </div>
                    </div>
                </div>
            `).join('');
        }

        // Auto Match uploaded photos to existing items
        function autoMatchPhotosToLedger() {
            let matchedAny = false;
            uploadedPhotos.forEach(p => {
                if (!p.assigned) {
                    const matchItem = auditItems.find(item => !item.photoUrl && (item.name.includes(p.tagKey) || item.usage.includes(p.tagKey)));
                    if (matchItem) {
                        matchItem.photoUrl = p.url;
                        matchItem.photoName = p.name;
                        matchItem.photoTags = p.tags;
                        p.assigned = true;
                        matchedAny = true;
                    }
                }
            });
            if (matchedAny) {
                runAIAudit();
            }
        }

        // Clear all photos
        function clearAllPhotos() {
            uploadedPhotos = [];
            auditItems.forEach(i => {
                i.photoUrl = null;
                i.photoName = null;
                i.photoTags = [];
            });
            renderPhotoGallery();
            runAIAudit();
            showToast("모든 증빙 사진이 삭제되었습니다.");
        }

        // Load Realistic 4 Presets
        function loadRealisticPreset() {
            uploadedPhotos = [];
            auditItems = JSON.parse(JSON.stringify(PRESET_CASES));
            
            // Populate photo gallery from presets
            auditItems.forEach(item => {
                if (item.photoUrl) {
                    uploadedPhotos.push({
                        id: Date.now() + Math.random(),
                        name: item.photoName,
                        url: item.photoUrl,
                        tags: item.photoTags,
                        tagKey: item.name.split(' ')[0],
                        assigned: true
                    });
                }
            });

            renderPhotoGallery();
            runAIAudit();
            showToast("4대 실무 케이스(적격/비계 부적격/스마트장비/신호수)가 로드되었습니다.");
        }

        // Core AI Cross-Verification & Legal Audit Engine
        function runAIAudit() {
            const smartLimit = totalBudget * 0.20;
            const workerLimit = totalBudget * 0.15;

            let currentSmartSum = 0;
            let currentWorkerSum = 0;

            // Audit Each Item
            auditItems.forEach(item => {
                const name = (item.name || "").toLowerCase();
                const usage = (item.usage || "").toLowerCase();
                const hasPhoto = Boolean(item.photoUrl);
                const tags = item.photoTags || [];

                let status = "APPROVED";
                let badgeText = "적격 승인";
                let reason = "";
                let legalBasis = "";
                let riskWarning = "";
                let requiredDocs = [];
                let photoMatchAnalysis = "";

                // 1. Scaffolding / Temporary Structure check (Strict Rejection)
                const isScaffold = name.includes("비계") || name.includes("작업발판") || usage.includes("비계") || usage.includes("발판") || tags.includes("외부비계") || tags.includes("시공성구조체");
                // 2. Traffic Signal personnel check (건진법 소관 불인정)
                const isTraffic = name.includes("신호수") || name.includes("유도원") || usage.includes("교통") || tags.includes("도로교통정리");

                if (isScaffold) {
                    // Check if it's pure safety net or whole scaffold
                    if ((name.includes("추락방지망") || name.includes("안전난간대")) && !name.includes("시스템 비계") && !name.includes("비계설치")) {
                        status = "WARNING";
                        badgeText = "보완 및 분리발주 필요";
                        reason = "가설 비계 본체와 안전시설(방망/난간)이 혼재되어 있습니다. 순수 안전시설 금액만 산안비로 정산 가능합니다.";
                        legalBasis = "고용노동부 고시 제7조 제2항: 가설 비계 본체는 시공원가(직접공사비) 항목으로 산안비 사용 불가.";
                        riskWarning = "비계 임대·설치비 전액 청구 시 근로감독관 점검에서 100% 삭감 및 환수 조치 위험.";
                        requiredDocs = ["비계 공사비와 안전시설 분리 산출내역서", "도면상 추락방지망 설치 구간 표시"];
                        photoMatchAnalysis = hasPhoto ? "⚠️ 사진상 외부 비계 구조체 본체가 식별됨 (시공성 구조물)" : "증빙 사진 누락";
                    } else {
                        status = "REJECTED";
                        badgeText = "부적격 (불인정/환수 대상)";
                        reason = "외부 비계, 시스템 비계, 작업발판은 시공 목적의 가설 구조물로서 산안비 집행이 절대 불가한 대표적 불인정 품목입니다.";
                        legalBasis = "고시 제7조 제2항 제1호: 공사의 시공·시공능률 증진을 위한 가설시설물은 산안비 불인정 대상.";
                        riskWarning = "대표적 환수 적발 사례 (도급내역 직접공사비 또는 공통가설비로 정산 계정 변경 필수).";
                        requiredDocs = ["산안비 청구 불가 - 공사 직접비 내역으로 계정 변경"];
                        photoMatchAnalysis = hasPhoto ? "❌ 사진 분석: 시공 목적 가설 비계 구조물 확인 (산안비 요건 미충족)" : "증빙 사진 없음";
                    }
                } else if (isTraffic) {
                    status = "REJECTED";
                    badgeText = "부적격 (건진법 소관)";
                    reason = "일반 도로 통행 및 덤프트럭 출입 유도용 교통신호수는 산안법이 아닌 건설기술진흥법(건진법)상 안전관리비 대상입니다.";
                    legalBasis = "노동부 고시 제7조 제1항 제1호 해석: 외부 공사차량 유도 및 원활한 공사 흐름 목적의 신호수는 산안비 불가.";
                    riskWarning = "건진법 항목을 산안비로 중복 이중청구 시 허위정산 적발 리스크.";
                    requiredDocs = ["발주처 건진법 안전관리비 항목으로 전용 정산 필요"];
                    photoMatchAnalysis = hasPhoto ? "❌ 사진 분석: 도로교통 유도 정황 확인 (공사현장 내부 전담 안전통제자 아님)" : "증빙 사진 없음";
                } else if (item.isSmart) {
                    // Smart safety tech check (20% limit)
                    currentSmartSum += item.amount;
                    if (currentSmartSum > smartLimit) {
                        status = "WARNING";
                        badgeText = "20% 한도 초과 (조건부 인정)";
                        reason = `스마트 안전장비 구입·임대 한도액(${formatKRW(smartLimit)})을 초과하였습니다. 초과분(${formatKRW(currentSmartSum - smartLimit)})은 인정되지 않을 수 있습니다.`;
                        legalBasis = "고시 제7조 제1항 제2호의2: 스마트 안전장비는 총 산안비의 20% 이내에서만 계상 인정.";
                        riskWarning = "한도 초과분 삭감 주의";
                    } else {
                        status = "APPROVED";
                        badgeText = "스마트장비 적격 인정";
                        reason = "지능형 센서 및 AI 기술을 활용한 스마트 안전장비로서 법정 20% 한도 내 적격 항목입니다.";
                        legalBasis = "고시 제7조 제1항 제2호의2 신설 조항 부합.";
                    }
                    requiredDocs = ["스마트 안전장비 도입 확인서", "통신 및 위험감지 기능 사양서", "위험성평가 회의록"];
                    photoMatchAnalysis = hasPhoto 
                        ? (tags.includes("스마트장비") || tags.includes("AI관제화면") ? "✅ 사진 분석: AI 모니터링 및 실시간 감지 화면 식별 완료" : "⚠️ 사진 분석: 단순 CCTV 외형만 확인됨 (통신·AI 기능 증빙 서류 보완 필요)")
                        : "❌ 스마트 장비 실물 및 모니터링 동작 화면 사진 필수 누락";
                    if (!hasPhoto) status = "WARNING";
                } else if (item.isWorker) {
                    // Worker autonomous check (15% limit)
                    currentWorkerSum += item.amount;
                    if (currentWorkerSum > workerLimit) {
                        status = "WARNING";
                        badgeText = "15% 한도 초과";
                        reason = `위험성평가·노사협의체 자율개선 품목 한도(${formatKRW(workerLimit)})를 초과하였습니다.`;
                        legalBasis = "고시 제7조 근로자 자율개선 품목 15% 한도 규정.";
                    } else {
                        status = "APPROVED";
                        badgeText = "자율개선 적격";
                        reason = "근로자 위험성평가 결과를 반영한 건강·작업환경 개선 품목입니다.";
                        legalBasis = "고시 제7조 근로자 의견 청취 및 노사협의체 의결 품목 인정 기준.";
                    }
                    requiredDocs = ["위험성평가 결과표 사본", "노사협의체 의결 회의록", "물품 수불대장(서명부)"];
                    photoMatchAnalysis = hasPhoto ? "✅ 현장 지급 및 착용 확인 사진 일치" : "⚠️ 물품 지급 대장 및 착용 증빙 사진 누락";
                    if (!hasPhoto) status = "WARNING";
                } else {
                    // Standard Category Items (Protective equipment, safety net, etc.)
                    if (item.category === 3) { // Protective gear
                        if (hasPhoto && tags.includes("KCs안전인증마크")) {
                            status = "APPROVED";
                            badgeText = "적격 (KCs 인증 확인)";
                            reason = "공인 KCs 안전인증을 필한 개인보호구로서 현장 지급 서명부 및 마크가 정확히 대조되었습니다.";
                            legalBasis = "고시 제7조 제1항 제3호: 법정 보호구 및 안전장구 구입비 100% 인정.";
                            photoMatchAnalysis = "✅ 사진 분석: KCs 안전인증 마크 및 보호구 지급 수령 서명부 완벽 일치";
                            requiredDocs = ["세금계산서", "보호구 지급대장(근로자 자필서명)", "KCs 인증서 사본"];
                        } else if (!hasPhoto) {
                            status = "WARNING";
                            badgeText = "보완 필요 (증빙 누락)";
                            reason = "품목 자체는 제3호 적격 품목이나, KCs 안전인증 마크 사진 및 근로자 수령 서명부가 등록되지 않았습니다.";
                            legalBasis = "산안법 안전인증기준 미달 제품 구매 방지를 위한 증빙 의무.";
                            photoMatchAnalysis = "❌ 증빙 사진 미등록: KCs 마크 및 지급대장 사진 업로드 필요";
                            requiredDocs = ["KCs 인증마크 식별 사진", "지급 서명부"];
                        } else {
                            status = "APPROVED";
                            badgeText = "적격";
                            reason = "제3호 보호구 항목에 부합합니다.";
                            legalBasis = "고시 제7조 제1항 제3호.";
                            photoMatchAnalysis = "ℹ️ 사진 등록 완료 (KCs 마크 추가 확인 권장)";
                            requiredDocs = ["세금계산서", "보호구 지급대장"];
                        }
                    } else {
                        // General safe items
                        status = "APPROVED";
                        badgeText = "적격 승인";
                        reason = `제${item.category}호 규정에 부합하는 현장 안전관리 적합 항목입니다.`;
                        legalBasis = `고용노동부 고시 제7조 제1항 제${item.category}호.`;
                        photoMatchAnalysis = hasPhoto ? "✅ 현장 설치 사진 검토 완료" : "⚠️ 현장 설치 전·후 증빙 사진 보완 권장";
                        requiredDocs = ["세금계산서/카드전표", "거래명세표", "현장 설치 사진"];
                    }
                }

                // Save Audit Outcome to Item
                item.auditStatus = status;
                item.badgeText = badgeText;
                item.auditReason = reason;
                item.legalBasis = legalBasis;
                item.riskWarning = riskWarning;
                item.requiredDocs = requiredDocs;
                item.photoMatchAnalysis = photoMatchAnalysis;
            });

            // Update Top Stats & UI
            updateDashboardMetrics(currentSmartSum, currentWorkerSum, smartLimit, workerLimit);
            renderAuditCards();
        }

        // Update Top Cards
        function updateDashboardMetrics(smartSum, workerSum, smartLimit, workerLimit) {
            const approvedTotal = auditItems
                .filter(i => i.auditStatus === 'APPROVED' || i.auditStatus === 'WARNING')
                .reduce((s, i) => s + i.amount, 0);

            const remaining = totalBudget - approvedTotal;
            const execRate = totalBudget > 0 ? ((approvedTotal / totalBudget) * 100).toFixed(1) : 0;

            document.getElementById('totalBudgetDisplay').innerText = formatKRW(totalBudget);
            document.getElementById('statApprovedAmount').innerText = formatKRW(approvedTotal);
            document.getElementById('statRemainingBudget').innerText = formatKRW(remaining);
            document.getElementById('execRateBadge').innerText = `${execRate}% 집행`;
            document.getElementById('execProgressBar').style.width = Math.min(execRate, 100) + '%';

            // Smart Tech Quota
            document.getElementById('smartUsedDisplay').innerText = formatKRW(smartSum);
            document.getElementById('smartLimitDisplay').innerText = `한도 ${formatKRW(smartLimit)}`;
            const smartRate = smartLimit > 0 ? ((smartSum / smartLimit) * 100).toFixed(1) : 0;
            const smartBar = document.getElementById('smartProgressBar');
            smartBar.style.width = Math.min(smartRate, 100) + '%';
            if (smartSum > smartLimit) {
                smartBar.className = "bg-red-500 h-2 rounded-full";
                document.getElementById('smartStatusBadge').className = "text-[11px] font-bold px-2 py-0.5 rounded bg-red-100 text-red-800";
                document.getElementById('smartStatusBadge').innerText = "한도 초과";
            } else {
                smartBar.className = "bg-blue-600 h-2 rounded-full";
                document.getElementById('smartStatusBadge').className = "text-[11px] font-bold px-2 py-0.5 rounded bg-blue-50 text-blue-700";
                document.getElementById('smartStatusBadge').innerText = `${smartRate}% 사용`;
            }

            // Worker Quota
            document.getElementById('workerUsedDisplay').innerText = formatKRW(workerSum);
            document.getElementById('workerLimitDisplay').innerText = `한도 ${formatKRW(workerLimit)}`;
            const workerRate = workerLimit > 0 ? ((workerSum / workerLimit) * 100).toFixed(1) : 0;
            const workerBar = document.getElementById('workerProgressBar');
            workerBar.style.width = Math.min(workerRate, 100) + '%';
            if (workerSum > workerLimit) {
                workerBar.className = "bg-red-500 h-2 rounded-full";
                document.getElementById('workerStatusBadge').className = "text-[11px] font-bold px-2 py-0.5 rounded bg-red-100 text-red-800";
                document.getElementById('workerStatusBadge').innerText = "한도 초과";
            } else {
                workerBar.className = "bg-purple-600 h-2 rounded-full";
                document.getElementById('workerStatusBadge').className = "text-[11px] font-bold px-2 py-0.5 rounded bg-purple-50 text-purple-700";
                document.getElementById('workerStatusBadge').innerText = `${workerRate}% 사용`;
            }

            // Update Summary Banner
            const banner = document.getElementById('auditSummaryBanner');
            if (auditItems.length > 0) {
                banner.classList.remove('hidden');
                const approvedCount = auditItems.filter(i => i.auditStatus === 'APPROVED').length;
                const rejectedCount = auditItems.filter(i => i.auditStatus === 'REJECTED').length;
                const warnCount = auditItems.filter(i => i.auditStatus === 'WARNING').length;
                const rejectedSum = auditItems.filter(i => i.auditStatus === 'REJECTED').reduce((s, i) => s + i.amount, 0);

                document.getElementById('auditSummaryHeading').innerText = 
                    `총 ${auditItems.length}건 중 적격 ${approvedCount}건, 부적격(불인정) ${rejectedCount}건, 보완필요 ${warnCount}건`;
                document.getElementById('auditSummaryDetail').innerText = 
                    rejectedCount > 0 
                    ? `불인정 대상 금액: ${formatKRW(rejectedSum)} (공사 직접비 또는 건진법 예산으로 즉시 전환 권고)`
                    : `현재 환수 위험 품목이 감지되지 않았습니다.`;
            } else {
                banner.classList.add('hidden');
            }
        }

        // Render Audit Cards
        function renderAuditCards() {
            const container = document.getElementById('auditItemsContainer');
            const empty = document.getElementById('auditEmptyState');

            let filtered = auditItems;
            if (activeFilter !== 'ALL') {
                filtered = auditItems.filter(i => i.auditStatus === activeFilter);
            }

            if (filtered.length === 0) {
                container.innerHTML = '';
                empty.classList.remove('hidden');
                return;
            }
            empty.classList.add('hidden');

            container.innerHTML = filtered.map(item => {
                let badgeStyle = "bg-emerald-100 text-emerald-800 border-emerald-300";
                let cardBorder = "border-slate-200";
                let statusIcon = "fa-solid fa-circle-check text-emerald-600";

                if (item.auditStatus === 'REJECTED') {
                    badgeStyle = "bg-red-100 text-red-800 border-red-300";
                    cardBorder = "border-red-200 bg-red-50/20";
                    statusIcon = "fa-solid fa-circle-xmark text-red-600";
                } else if (item.auditStatus === 'WARNING') {
                    badgeStyle = "bg-amber-100 text-amber-800 border-amber-300";
                    cardBorder = "border-amber-200 bg-amber-50/20";
                    statusIcon = "fa-solid fa-triangle-exclamation text-amber-600";
                }

                return `
                <div class="bg-white rounded-xl border ${cardBorder} p-4 sm:p-5 shadow-sm space-y-4 hover:shadow-md transition">
                    
                    <!-- Item Header & Outcome Badges -->
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
                        <div class="flex items-start sm:items-center gap-3">
                            <i class="${statusIcon} text-xl mt-0.5 sm:mt-0"></i>
                            <div>
                                <div class="flex items-center gap-2 flex-wrap">
                                    <span class="text-xs font-bold text-slate-500 bg-slate-100 px-2 py-0.5 rounded">
                                        ${CATEGORIES[item.category] || '제2호 안전시설비'}
                                    </span>
                                    <h4 class="text-sm sm:text-base font-extrabold text-slate-900">${item.name}</h4>
                                    ${item.isSmart ? '<span class="text-[10px] font-bold bg-blue-100 text-blue-800 px-1.5 py-0.5 rounded">스마트 20%</span>' : ''}
                                    ${item.isWorker ? '<span class="text-[10px] font-bold bg-purple-100 text-purple-800 px-1.5 py-0.5 rounded">노사자율 15%</span>' : ''}
                                </div>
                                <p class="text-xs text-slate-500 mt-1"><i class="fa-solid fa-location-dot text-slate-400 mr-1"></i>사용 목적: ${item.usage}</p>
                            </div>
                        </div>

                        <div class="flex items-center justify-between sm:justify-end gap-3 self-end sm:self-auto">
                            <span class="text-base sm:text-lg font-black text-slate-900">${formatKRW(item.amount)}</span>
                            <span class="text-xs font-bold px-3 py-1 rounded-full border ${badgeStyle} flex items-center gap-1.5 whitespace-nowrap">
                                ${item.badgeText}
                            </span>
                            <button onclick="deleteAuditItem(${item.id})" class="text-slate-400 hover:text-red-500 p-1.5 transition no-print" title="삭제">
                                <i class="fa-solid fa-trash-can"></i>
                            </button>
                        </div>
                    </div>

                    <!-- Twin Check Grid: Legal Judgment vs Photo Evidence -->
                    <div class="grid grid-cols-1 md:grid-cols-12 gap-4 text-xs">
                        
                        <!-- Left: Legal Criteria (7 cols) -->
                        <div class="md:col-span-8 space-y-2">
                            <div class="bg-slate-50 p-3 rounded-xl border border-slate-200">
                                <div class="font-bold text-slate-800 mb-1 flex items-center gap-1.5">
                                    <i class="fa-solid fa-scale-balanced text-slate-500"></i> AI 판단 사유 및 고시 해석
                                </div>
                                <p class="text-slate-700 leading-relaxed">${item.auditReason}</p>
                                <div class="text-[11px] text-slate-500 mt-1.5 font-medium">${item.legalBasis}</div>
                            </div>

                            ${item.riskWarning ? `
                                <div class="bg-red-50 text-red-900 p-2.5 rounded-xl border border-red-200 flex items-start gap-2">
                                    <i class="fa-solid fa-triangle-exclamation text-red-600 mt-0.5"></i>
                                    <div>
                                        <strong class="font-bold">환수 리스크 경고:</strong> ${item.riskWarning}
                                    </div>
                                </div>
                            ` : ''}

                            <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-200">
                                <span class="font-bold text-slate-700 block mb-1">필수 구비 증빙서류:</span>
                                <div class="flex flex-wrap gap-1.5">
                                    ${item.requiredDocs.map(doc => `
                                        <span class="bg-white border border-slate-300 text-slate-700 px-2 py-0.5 rounded text-[11px] flex items-center gap-1">
                                            <i class="fa-regular fa-file-lines text-slate-400"></i> ${doc}
                                        </span>
                                    `).join('')}
                                </div>
                            </div>
                        </div>

                        <!-- Right: Matched Photo & Tag Evidence (4 cols) -->
                        <div class="md:col-span-4 bg-slate-50 p-3 rounded-xl border border-slate-200 flex flex-col justify-between">
                            <div>
                                <div class="font-bold text-slate-800 mb-2 flex items-center justify-between">
                                    <span class="flex items-center gap-1.5"><i class="fa-solid fa-camera text-slate-500"></i> 현장 증빙 사진 대조</span>
                                    ${item.photoUrl ? '<span class="text-[10px] text-emerald-700 bg-emerald-100 px-1.5 py-0.5 rounded font-bold">사진 매칭됨</span>' : '<span class="text-[10px] text-slate-400 bg-slate-200 px-1.5 py-0.5 rounded">사진 미등록</span>'}
                                </div>

                                ${item.photoUrl ? `
                                    <div class="flex gap-2.5 items-center">
                                        <img src="${item.photoUrl}" alt="증빙" class="w-16 h-16 object-cover rounded-lg border border-slate-300 shadow-inner cursor-pointer" onclick="viewPhotoDirect('${item.photoUrl}', '${item.name}', '${(item.photoTags || []).join(', ')}')">
                                        <div class="space-y-1">
                                            <div class="text-[11px] font-bold text-slate-800 truncate max-w-[130px]">${item.photoName || '증빙사진.jpg'}</div>
                                            <div class="flex flex-wrap gap-1">
                                                ${(item.photoTags || []).map(t => `<span class="bg-slate-200 text-slate-700 text-[9px] px-1 rounded">${t}</span>`).join('')}
                                            </div>
                                        </div>
                                    </div>
                                ` : `
                                    <div class="text-center py-4 bg-white rounded-lg border border-dashed border-slate-300 text-slate-400">
                                        <i class="fa-regular fa-image text-2xl mb-1"></i>
                                        <p class="text-[11px]">매칭된 사진 증빙 없음</p>
                                    </div>
                                `}
                            </div>

                            <div class="mt-2 pt-2 border-t border-slate-200 text-[11px] leading-snug">
                                <span class="font-semibold text-slate-700">대조 결과:</span>
                                <span class="text-slate-600 ml-1">${item.photoMatchAnalysis}</span>
                            </div>
                        </div>

                    </div>
                </div>
                `;
            }).join('');
        }

        // Delete single audit item
        function deleteAuditItem(id) {
            auditItems = auditItems.filter(i => i.id !== id);
            runAIAudit();
            showToast("항목이 삭제되었습니다.");
        }

        // Filter Audit Table
        function filterAuditTable(status) {
            activeFilter = status;
            renderAuditCards();
        }

        // Export Report to CSV
        function exportAuditReportCSV() {
            if (auditItems.length === 0) {
                showToast("내보낼 검토 결과가 없습니다.", false);
                return;
            }

            let csvContent = "\uFEFF"; // UTF-8 BOM
            csvContent += "구분,품목명,금액(원),용도,스마트장비(20%),근로자자율(15%),적격여부,AI판정사유,법적근거,증빙사진유무\n";

            auditItems.forEach(item => {
                const row = [
                    `"${CATEGORIES[item.category] || '제2호'}"`,
                    `"${(item.name || '').replace(/"/g, '""')}"`,
                    item.amount,
                    `"${(item.usage || '').replace(/"/g, '""')}"`,
                    item.isSmart ? "Y" : "N",
                    item.isWorker ? "Y" : "N",
                    item.badgeText,
                    `"${(item.auditReason || '').replace(/"/g, '""')}"`,
                    `"${(item.legalBasis || '').replace(/"/g, '""')}"`,
                    item.photoUrl ? "Y" : "N"
                ];
                csvContent += row.join(",") + "\n";
            });

            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.setAttribute('href', url);
            link.setAttribute('download', `산안비_지출및증빙대조_검토보고서_${new Date().toISOString().slice(0,10)}.csv`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            showToast("엑셀(CSV) 보고서가 다운로드되었습니다.");
        }

        // Modal Helpers
        function openImageModal(idx) {
            const p = uploadedPhotos[idx];
            if (!p) return;
            document.getElementById('modalImgTitle').innerText = p.name;
            document.getElementById('modalImgElement').src = p.url;
            document.getElementById('modalImgTags').innerText = p.tags.join(', ');
            
            const matchedItem = auditItems.find(i => i.photoUrl === p.url);
            document.getElementById('modalImgMatch').innerText = matchedItem ? matchedItem.name : "미지정 (자동 대조 대기)";

            document.getElementById('imageDetailModal').classList.remove('hidden');
        }

        function viewPhotoDirect(url, name, tags) {
            document.getElementById('modalImgTitle').innerText = name;
            document.getElementById('modalImgElement').src = url;
            document.getElementById('modalImgTags').innerText = tags || "인증마크, 실물";
            document.getElementById('modalImgMatch').innerText = name;
            document.getElementById('imageDetailModal').classList.remove('hidden');
        }

        function closeImageModal() {
            document.getElementById('imageDetailModal').classList.add('hidden');
        }

        function openBudgetModal() {
            document.getElementById('inputBudgetModal').value = totalBudget;
            document.getElementById('budgetModal').classList.remove('hidden');
        }

        function closeBudgetModal() {
            document.getElementById('budgetModal').classList.add('hidden');
        }

        function saveBudgetModal() {
            const val = parseInt(document.getElementById('inputBudgetModal').value, 10);
            if (isNaN(val) || val <= 0) {
                showToast("유효한 금액을 입력해주세요.", false);
                return;
            }
            totalBudget = val;
            closeBudgetModal();
            runAIAudit();
            showToast("총 예산이 성공적으로 반영되었습니다.");
        }

        // Window Init
        window.onload = function() {
            // Load realistic cases by default for interactive first experience
            loadRealisticPreset();
        };
    </script>
</body>
</html>