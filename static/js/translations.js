// 雙語翻譯資料
const translations = {
    'zh-TW': {
        // Navbar
        'nav.brand': 'Minic',
        'nav.home': '首頁',
        'nav.about': '關於',
        'nav.explore': '探索',
        'nav.share': '分享',
        'nav.add_database': '新增資料庫',

        // Hero Section
        'hero.title': '臺北醫學大學 神經學研究資料庫平台',
        'hero.subtitle': '整合多個神經學研究資料庫，提供研究人員資料存取、分析工具和合作平台',
        'hero.search_placeholder': '搜尋資料庫...',
        'hero.search_button': '搜尋',

        // Filters
        'filter.resource_type': '資源類型',
        'filter.database': '資料庫',
        'filter.software': '軟體',
        'filter.tutorial': '教學',
        'filter.challenge': '挑戰',
        'filter.access': '存取權限',
        'filter.open_access': '開放存取',
        'filter.restricted_access': '限制存取',
        'filter.sort_by': '排序方式',
        'filter.relevance': '相關性',
        'filter.latest': '最新',
        'filter.oldest': '最舊',
        'filter.title_asc': '標題 (升序)',
        'filter.title_desc': '標題 (降序)',
        'filter.size_asc': '大小 (升序)',
        'filter.size_desc': '大小 (降序)',
        'filter.apply': '套用篩選',

        // Resources Section
        'resources.title': '資源',
        'resources.published': '發布日期',
        'resources.version': '版本',
        'resources.data_period': '資料期間',
        'resources.evaluation_standard': '評估標準',
        'resources.size': '大小',
        'resources.status': '狀態',
        'resources.language': '語言',
        'resources.download': '下載',
        'resources.details': '詳細資訊',
        'resources.coming_soon': '即將開放',
        'resources.github': 'GitHub',

        // Database Detail Page Labels
        'detail.open_access': '開放存取',
        'detail.restricted_access': '限制存取',
        'detail.published_date': '發布日期',
        'detail.version': '版本',
        'detail.cite_resource': '引用此資源時，請引用：',
        'detail.apa_format': 'APA 格式',
        'detail.mla_format': 'MLA 格式',
        'detail.chicago_format': 'Chicago 格式',
        'detail.harvard_format': 'Harvard 格式',
        'detail.vancouver_format': 'Vancouver 格式',
        'detail.abstract': '摘要',
        'detail.background': '背景',
        'detail.methods': '方法',
        'detail.data_description': '資料描述',
        'detail.data_files': '資料檔案：',
        'detail.records': '筆記錄',
        'detail.usage_notes': '使用說明',
        'detail.release_notes': '發布說明',
        'detail.ethics': '倫理',
        'detail.acknowledgments': '致謝',
        'detail.conflicts': '利益衝突',
        'detail.references': '參考文獻',
        'detail.view_paper': '查看論文',
        'detail.files_downloads': '檔案和下載',
        'detail.download_full': '下載完整資料集',
        'detail.download_anonymized': '下載去識別化資料',
        'detail.view_on_github': '在 GitHub 上查看',
        'detail.access_policy': '存取政策',
        'detail.license': '授權條款',
        'detail.topics': '主題',
        'detail.share': '分享',
        'detail.access': '存取',
        'detail.access_policy_label': '存取政策：',
        'detail.license_label': '授權 (檔案)：',
        'detail.discovery': '發現',
        'detail.doi': 'DOI (最新版本)：',
        'detail.topics_label': '主題：',
        'detail.project_website': '專案網站：',
        'detail.files': '檔案',
        'detail.total_size': '總未壓縮大小',
        'detail.access_files': '存取檔案',
        'detail.download_zip': '下載 ZIP 檔案',
        'detail.terminal_download': '使用終端機下載檔案：',
        'detail.aws_download': '使用 AWS 命令列工具下載檔案，請先配置您的 AWS 憑證。',
        'detail.versions': '版本',
        'detail.corresponding_member': '通訊作者',
        'detail.contact': '聯絡',
        'detail.share_title': '分享',

        // Footer
        'footer.platform_desc': '臺北醫學大學神經學研究資料庫平台',
        'footer.platform_subdesc': '整合多個神經學研究資料庫，促進神經科學研究發展',
        'footer.explore_title': '探索',
        'footer.databases': '資料庫',
        'footer.software': '軟體',
        'footer.tutorials': '教學',
        'footer.challenges': '挑戰',
        'footer.contact_title': '聯絡資訊',
        'footer.copyright': '臺北醫學大學 神經學研究資料庫平台 | 參考',
        'footer.design_ref': '設計，品牌為 Minic',
        'footer.explore_resources': '探索資源',
        'footer.share_database': '分享資料庫',
        'footer.about_platform': '關於平台',
        'footer.database_details': '資料庫詳情',

        // Database 1: Dementia
        'db1.badge_type': '資料庫',
        'db1.badge_access': '開放存取',
        'db1.title': '臺灣失智症臨床資料庫',
        'db1.authors': '臺北醫學大學雙和醫院失智症中心與神經內科研究團隊',
        'db1.description_1': '這項研究採用臺北醫學大學雙和醫院失智症中心與神經內科的受試者資料，建立了以阿茲海默症患者為核心的臨床資料庫。該資料庫收錄符合美國國家老化研究院-阿茲海默症協會(NIA-AA)標準的疑似AD患者，收集的內容包含病歷、神經心理評估（如MMSE、CASI、CDR）、持續多年的追蹤數據及部分患者的腦部MRI影像。所有數據經過嚴格去識別化處理，並遵照研究倫理規範，包含人口統計、病程、教育年數、神經心理多領域測驗分數、臨床失智嚴重度、腦萎縮與白質病灶評分等詳細變項。',
        'db1.description_2': '該資料庫的患者涵蓋輕至中度阿茲海默症，具備多次年度評估紀錄與完整隨訪資料。研究團隊將神經心理評估各面向結合機器學習方法進行異質性分類，促進亞型分群分析。這樣的資料庫可應用於阿茲海默症異質性研究、疾病進展模式分析、個體化治療標的開發與跨中心橫斷及縱貫研究協作，是台灣區域極具代表性且結構嚴謹的失智症臨床資料資源。',
        'db1.publications_title': '相關研究論文',
        'db1.publication_title': 'Heterogeneity of Alzheimer\'s disease identified by neuropsychological test profiling',
        'db1.publication_citation': 'Nguyen TTT, Lee HH, Huang LK, et al. PLoS One. 2023;18(10):e0292527.',
        'db1.publication_description': '本研究採用神經心理測試分析識別阿茲海默症的異質性，使用機器學習方法進行認知亞型分群分析。',

        // Database 1 Content (Dynamic)
        'db1.abstract_content': '這項研究採用臺北醫學大學雙和醫院失智症中心與神經內科的受試者資料，建立了以阿茲海默症患者為核心的臨床資料庫。該資料庫收錄符合美國國家老化研究院-阿茲海默症協會(NIA-AA)標準的疑似AD患者，收集的內容包含病歷、神經心理評估（如MMSE、CASI、CDR）、持續多年的追蹤數據及部分患者的腦部MRI影像。所有數據經過嚴格去識別化處理，並遵照研究倫理規範，包含人口統計、病程、教育年數、神經心理多領域測驗分數、臨床失智嚴重度、腦萎縮與白質病灶評分等詳細變項。',
        'db1.background_content': '該資料庫的患者涵蓋輕至中度阿茲海默症，具備多次年度評估紀錄與完整隨訪資料。研究團隊將神經心理評估各面向結合機器學習方法進行異質性分類，促進亞型分群分析。',
        'db1.methods_content': '資料收集採用標準化神經心理評估工具，包括MMSE、CASI、CDR等量表。所有數據經過嚴格去識別化處理，確保患者隱私保護。',
        'db1.data_description_content': '資料庫包含多個CSV檔案，涵蓋患者基本資訊、診斷結果、認知測試分數、腦部影像評分等。',
        'db1.usage_notes_content': '本資料庫僅供研究使用，使用者需遵守相關倫理規範和資料使用協議。',
        'db1.release_notes_content': '初始版本包含2012-2024年收案資料，經過去識別化處理後發布。',
        'db1.ethics_content': '本研究已通過臺北醫學大學人體試驗委員會審查，所有參與者均簽署知情同意書，所有參與者均可自動退出。',
        'db1.acknowledgments_content': '感謝所有參與研究的患者及其家屬，以及研究團隊成員的貢獻。',
        'db1.conflicts_content': '研究團隊聲明無利益衝突。',

        // Database 1 Tags
        'tag.alzheimers': '阿茲海默症',
        'tag.neuropsych': '神經心理評估',
        'tag.mmse': 'MMSE',
        'tag.casi': 'CASI',
        'tag.cdr': 'CDR',
        'tag.brain_mri': '腦部MRI',
        'tag.machine_learning': '機器學習',
        'tag.heterogeneity': '異質性分析',

        // Database 2 Tags
        'tag.consciousness': '意識研究',
        'tag.eeg': '腦電圖',
        'tag.fmri': 'fMRI',
        'tag.multimodal': '多模態',

        // Database 3 Tags
        'tag.python': 'Python',
        'tag.neuroimaging': '神經影像',

        // Database 2: Consciousness
        'db2.badge_type': '資料庫',
        'db2.badge_access': '限制存取',
        'db2.title': '大腦意識資料庫',
        'db2.authors': '臺北醫學大學腦科學研究中心',
        'db2.description': '研究大腦意識狀態、認知功能和神經可塑性的綜合資料庫，包含腦電圖、功能性磁振造影等多模態資料。專注於意識研究，為神經科學研究提供豐富的數據資源。',

        // Software
        'soft1.badge_type': '軟體',
        'soft1.badge_access': '開放存取',
        'soft1.title': '神經影像分析工具包',
        'soft1.authors': '臺北醫學大學醫學影像實驗室',
        'soft1.description': '專為神經影像分析設計的 Python 工具包，支援腦電圖、功能性磁振造影、擴散張量影像等多種神經影像格式的處理和分析。',

        // Explore Section
        'explore.title': '探索更多資源',
        'explore.tutorial_title': '教學資源',
        'explore.tutorial_desc': '探索神經科學相關的教學材料、課程和學習資源，提升研究技能和知識水平。',
        'explore.tutorial_button': '瀏覽教學資源',
        'explore.challenge_title': '研究挑戰',
        'explore.challenge_desc': '參與神經科學研究挑戰，與其他研究人員競賽，推動創新研究發展。',
        'explore.challenge_button': '查看挑戰',

        // Share Section
        'share.title': '分享您的資料庫',
        'share.description': '您有神經學研究資料庫想要分享嗎？我們歡迎研究人員提交新的資料庫，共同推進神經科學研究發展。',
        'share.why_title': '為什麼要分享？',
        'share.why_1': '增加研究影響力和可見度',
        'share.why_2': '促進跨機構研究合作',
        'share.why_3': '為神經科學研究社群做出貢獻',
        'share.why_4': '獲得專業的資料管理和發布支援',
        'share.types_title': '支援的資料類型',
        'share.types_1': '臨床研究資料',
        'share.types_2': '神經影像資料',
        'share.types_3': '基因組學資料',
        'share.types_4': '行為研究資料',
        'share.types_5': '軟體工具和腳本',
        'share.button': '開始提交資料庫',

        // Footer
        'footer.platform_name': 'Minic',
        'footer.platform_desc': '臺北醫學大學神經學研究資料庫平台',
        'footer.platform_tagline': '整合多個神經學研究資料庫，促進神經科學研究發展',
        'footer.explore': '探索',
        'footer.explore_resources': '探索資源',
        'footer.share_database': '分享資料庫',
        'footer.about_platform': '關於平台',
        'footer.database_details': '資料庫詳情',
        'footer.contact': '聯絡資訊',
        'footer.copyright': '臺北醫學大學 神經學研究資料庫平台 | 參考',
        'footer.copyright_2': '設計，品牌為 Minic',

        // Messages
        'msg.loading': '載入中...',
        'msg.loading_resource': '載入資源詳情...',
        'msg.searching': '正在搜尋',
        'msg.applying_filters': '正在套用篩選...',
        'msg.filters_applied': '篩選已套用',
        'msg.search_result': '已搜尋',
    },

    'en': {
        // Navbar
        'nav.brand': 'Minic',
        'nav.home': 'Home',
        'nav.about': 'About',
        'nav.explore': 'Explore',
        'nav.share': 'Share',
        'nav.add_database': 'Add Database',

        // Hero Section
        'hero.title': 'Taipei Medical University Neurology Research Database Platform',
        'hero.subtitle': 'Integrating multiple neurology research databases to provide researchers with data access, analysis tools, and collaboration platforms',
        'hero.search_placeholder': 'Search databases...',
        'hero.search_button': 'Search',

        // Filters
        'filter.resource_type': 'Resource Type',
        'filter.database': 'Database',
        'filter.software': 'Software',
        'filter.tutorial': 'Tutorial',
        'filter.challenge': 'Challenge',
        'filter.access': 'Access',
        'filter.open_access': 'Open Access',
        'filter.restricted_access': 'Restricted Access',
        'filter.sort_by': 'Sort By',
        'filter.relevance': 'Relevance',
        'filter.latest': 'Latest',
        'filter.oldest': 'Oldest',
        'filter.title_asc': 'Title (Asc)',
        'filter.title_desc': 'Title (Desc)',
        'filter.size_asc': 'Size (Asc)',
        'filter.size_desc': 'Size (Desc)',
        'filter.apply': 'Apply Filters',

        // Resources Section
        'resources.title': 'Resources',
        'resources.published': 'Published',
        'resources.version': 'Version',
        'resources.data_period': 'Data Period',
        'resources.evaluation_standard': 'Evaluation Standard',
        'resources.size': 'Size',
        'resources.status': 'Status',
        'resources.language': 'Language',
        'resources.download': 'Download',
        'resources.details': 'Details',
        'resources.coming_soon': 'Coming Soon',
        'resources.github': 'GitHub',

        // Database Detail Page Labels
        'detail.open_access': 'Open Access',
        'detail.restricted_access': 'Restricted Access',
        'detail.published_date': 'Published',
        'detail.version': 'Version',
        'detail.cite_resource': 'When citing this resource, please cite:',
        'detail.apa_format': 'APA Format',
        'detail.mla_format': 'MLA Format',
        'detail.chicago_format': 'Chicago Format',
        'detail.harvard_format': 'Harvard Format',
        'detail.vancouver_format': 'Vancouver Format',
        'detail.abstract': 'Abstract',
        'detail.background': 'Background',
        'detail.methods': 'Methods',
        'detail.data_description': 'Data Description',
        'detail.data_files': 'Data Files:',
        'detail.records': 'records',
        'detail.usage_notes': 'Usage Notes',
        'detail.release_notes': 'Release Notes',
        'detail.ethics': 'Ethics',
        'detail.acknowledgments': 'Acknowledgments',
        'detail.conflicts': 'Conflicts of Interest',
        'detail.references': 'References',
        'detail.view_paper': 'View Paper',
        'detail.files_downloads': 'Files and Downloads',
        'detail.download_full': 'Download Full Dataset',
        'detail.download_anonymized': 'Download Anonymized Data',
        'detail.view_on_github': 'View on GitHub',
        'detail.access_policy': 'Access Policy',
        'detail.license': 'License',
        'detail.topics': 'Topics',
        'detail.share': 'Share',
        'detail.access': 'Access',
        'detail.access_policy_label': 'Access Policy:',
        'detail.license_label': 'License (for files):',
        'detail.discovery': 'Discovery',
        'detail.doi': 'DOI (latest version):',
        'detail.topics_label': 'Topics:',
        'detail.project_website': 'Project Website:',
        'detail.files': 'Files',
        'detail.total_size': 'Total uncompressed size',
        'detail.access_files': 'Access the files',
        'detail.download_zip': 'Download the ZIP file',
        'detail.terminal_download': 'Download the files using your terminal:',
        'detail.aws_download': 'Download the files using the AWS Command Line Interface, please configure your AWS credentials first.',
        'detail.versions': 'Versions',
        'detail.corresponding_member': 'Corresponding Member',
        'detail.contact': 'Contact',
        'detail.share_title': 'Share',

        // Footer
        'footer.platform_desc': 'Taipei Medical University Neurology Research Database Platform',
        'footer.platform_subdesc': 'Integrating multiple neurology research databases to advance neuroscience research',
        'footer.explore_title': 'Explore',
        'footer.databases': 'Databases',
        'footer.software': 'Software',
        'footer.tutorials': 'Tutorials',
        'footer.challenges': 'Challenges',
        'footer.contact_title': 'Contact',
        'footer.copyright': 'Taipei Medical University Neurology Research Database Platform | Inspired by',
        'footer.design_ref': 'design, branded as Minic',
        'footer.explore_resources': 'Explore Resources',
        'footer.share_database': 'Share Database',
        'footer.about_platform': 'About Platform',
        'footer.database_details': 'Database Details',

        // Database 1: Dementia
        'db1.badge_type': 'Database',
        'db1.badge_access': 'Open Access',
        'db1.title': 'Taiwan Dementia Clinical Database',
        'db1.authors': 'TMU Shuang Ho Hospital Dementia Center and Neurology Research Team',
        'db1.description_1': 'This study utilizes patient data from the Dementia Center and Department of Neurology at Taipei Medical University\'s Shuang Ho Hospital to establish a clinical database centered on Alzheimer\'s disease (AD) patients. The database includes suspected AD patients who meet the National Institute on Aging-Alzheimer\'s Association (NIA-AA) criteria. Collected data encompasses medical records, neuropsychological assessments (such as MMSE, CASI, CDR), multi-year follow-up data, and brain MRI images for some patients. All data has undergone strict de-identification and complies with research ethics standards, including detailed variables such as demographics, disease course, years of education, neuropsychological multi-domain test scores, clinical dementia severity, brain atrophy and white matter lesion scores.',
        'db1.description_2': 'The database patients cover mild to moderate Alzheimer\'s disease, with multiple annual assessment records and complete follow-up data. The research team combines various aspects of neuropsychological assessment with machine learning methods for heterogeneity classification, promoting subtype clustering analysis. This database can be applied to Alzheimer\'s disease heterogeneity research, disease progression pattern analysis, individualized treatment target development, and cross-center cross-sectional and longitudinal research collaboration. It is a highly representative and structurally rigorous clinical dementia data resource in the Taiwan region.',
        'db1.publications_title': 'Related Publications',
        'db1.publication_title': 'Heterogeneity of Alzheimer\'s disease identified by neuropsychological test profiling',
        'db1.publication_citation': 'Nguyen TTT, Lee HH, Huang LK, et al. PLoS One. 2023;18(10):e0292527.',
        'db1.publication_description': 'This study uses neuropsychological test analysis to identify heterogeneity in Alzheimer\'s disease, employing machine learning methods for cognitive subtype clustering analysis.',

        // Database 1 Content (Dynamic)
        'db1.abstract_content': 'This study utilizes patient data from the Dementia Center and Department of Neurology at Taipei Medical University\'s Shuang Ho Hospital to establish a clinical database centered on Alzheimer\'s disease (AD) patients. The database includes suspected AD patients who meet the National Institute on Aging-Alzheimer\'s Association (NIA-AA) criteria. Collected data encompasses medical records, neuropsychological assessments (such as MMSE, CASI, CDR), multi-year follow-up data, and brain MRI images for some patients. All data has undergone strict de-identification and complies with research ethics standards, including detailed variables such as demographics, disease course, years of education, neuropsychological multi-domain test scores, clinical dementia severity, brain atrophy and white matter lesion scores.',
        'db1.background_content': 'The database includes patients with mild to moderate Alzheimer\'s disease, with multiple annual assessment records and complete follow-up data. The research team combines various aspects of neuropsychological assessment with machine learning methods for heterogeneity classification, promoting subtype clustering analysis.',
        'db1.methods_content': 'Data collection employs standardized neuropsychological assessment tools, including MMSE, CASI, CDR and other scales. All data has undergone strict de-identification to ensure patient privacy protection.',
        'db1.data_description_content': 'The database contains multiple CSV files, covering patient basic information, diagnostic results, cognitive test scores, brain imaging scores, etc.',
        'db1.usage_notes_content': 'This database is for research use only. Users must comply with relevant ethical standards and data use agreements.',
        'db1.release_notes_content': 'Initial version contains data collected from 2012-2024, published after de-identification processing.',
        'db1.ethics_content': 'This study has been approved by the Taipei Medical University Institutional Review Board. All participants signed informed consent forms and can withdraw at any time.',
        'db1.acknowledgments_content': 'We thank all patients and their families who participated in the research, as well as the contributions of research team members.',
        'db1.conflicts_content': 'The research team declares no conflicts of interest.',

        // Database 1 Tags
        'tag.alzheimers': 'Alzheimer\'s Disease',
        'tag.neuropsych': 'Neuropsychological Assessment',
        'tag.mmse': 'MMSE',
        'tag.casi': 'CASI',
        'tag.cdr': 'CDR',
        'tag.brain_mri': 'Brain MRI',
        'tag.machine_learning': 'Machine Learning',
        'tag.heterogeneity': 'Heterogeneity Analysis',

        // Database 2 Tags
        'tag.consciousness': 'Consciousness Research',
        'tag.eeg': 'EEG',
        'tag.fmri': 'fMRI',
        'tag.multimodal': 'Multimodal',

        // Database 3 Tags
        'tag.python': 'Python',
        'tag.neuroimaging': 'Neuroimaging',

        // Database 2: Consciousness
        'db2.badge_type': 'Database',
        'db2.badge_access': 'Restricted Access',
        'db2.title': 'Brain Consciousness Database',
        'db2.authors': 'TMU Brain Science Research Center',
        'db2.description': 'A comprehensive database for studying brain consciousness states, cognitive functions, and neuroplasticity, including multimodal data such as electroencephalography and functional magnetic resonance imaging. Focused on consciousness research, providing rich data resources for neuroscience research.',

        // Software
        'soft1.badge_type': 'Software',
        'soft1.badge_access': 'Open Access',
        'soft1.title': 'Neuroimaging Analysis Toolkit',
        'soft1.authors': 'TMU Medical Imaging Laboratory',
        'soft1.description': 'A Python toolkit specifically designed for neuroimaging analysis, supporting processing and analysis of various neuroimaging formats including EEG, functional MRI, and diffusion tensor imaging.',

        // Explore Section
        'explore.title': 'Explore More Resources',
        'explore.tutorial_title': 'Educational Resources',
        'explore.tutorial_desc': 'Explore neuroscience-related teaching materials, courses, and learning resources to enhance research skills and knowledge.',
        'explore.tutorial_button': 'Browse Educational Resources',
        'explore.challenge_title': 'Research Challenges',
        'explore.challenge_desc': 'Participate in neuroscience research challenges, compete with other researchers, and drive innovative research development.',
        'explore.challenge_button': 'View Challenges',

        // Share Section
        'share.title': 'Share Your Database',
        'share.description': 'Do you have a neurology research database you would like to share? We welcome researchers to submit new databases and jointly advance neuroscience research development.',
        'share.why_title': 'Why Share?',
        'share.why_1': 'Increase research impact and visibility',
        'share.why_2': 'Promote cross-institutional research collaboration',
        'share.why_3': 'Contribute to the neuroscience research community',
        'share.why_4': 'Receive professional data management and publication support',
        'share.types_title': 'Supported Data Types',
        'share.types_1': 'Clinical research data',
        'share.types_2': 'Neuroimaging data',
        'share.types_3': 'Genomics data',
        'share.types_4': 'Behavioral research data',
        'share.types_5': 'Software tools and scripts',
        'share.button': 'Start Submitting Database',

        // Footer
        'footer.platform_name': 'Minic',
        'footer.platform_desc': 'Taipei Medical University Neurology Research Database Platform',
        'footer.platform_tagline': 'Integrating multiple neurology research databases to advance neuroscience research',
        'footer.explore': 'Explore',
        'footer.explore_resources': 'Explore Resources',
        'footer.share_database': 'Share Database',
        'footer.about_platform': 'About Platform',
        'footer.database_details': 'Database Details',
        'footer.contact': 'Contact Information',
        'footer.copyright': 'Taipei Medical University Neurology Research Database Platform | Inspired by',
        'footer.copyright_2': 'design, branded as Minic',

        // Messages
        'msg.loading': 'Loading...',
        'msg.loading_resource': 'Loading resource details...',
        'msg.searching': 'Searching',
        'msg.applying_filters': 'Applying filters...',
        'msg.filters_applied': 'Filters applied',
        'msg.search_result': 'Searched',
    }
};

// 語言切換功能
class LanguageManager {
    constructor() {
        this.currentLang = localStorage.getItem('language') || 'zh-TW';
        this.init();
    }

    init() {
        // 設定初始語言
        this.setLanguage(this.currentLang, false);

        // 綁定語言切換按鈕事件（不需要再包 DOMContentLoaded，因為外層已經有了）
        this.bindLanguageSwitchers();
    }

    bindLanguageSwitchers() {
        const langButtons = document.querySelectorAll('[data-lang]');
        console.log('Found language buttons:', langButtons.length);

        langButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const lang = button.getAttribute('data-lang');
                console.log('Switching to:', lang);
                this.setLanguage(lang);
            });
        });
    }

    setLanguage(lang, save = true) {
        this.currentLang = lang;

        if (save) {
            localStorage.setItem('language', lang);
        }

        // 更新 HTML lang 屬性
        document.documentElement.lang = lang;

        // 更新所有翻譯元素
        this.updateTranslations();

        // 更新語言按鈕狀態
        this.updateLanguageButtons();
    }

    updateTranslations() {
        // 處理 data-i18n 屬性（UI 標籤）
        const elements = document.querySelectorAll('[data-i18n]');
        elements.forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.getTranslation(key);

            if (translation) {
                if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                    element.placeholder = translation;
                } else if (element.tagName === 'OPTION') {
                    element.textContent = translation;
                } else {
                    // 對於普通元素，直接設置 textContent
                    element.textContent = translation;
                }
            }
        });

        // 特別處理 select 元素內的 option
        document.querySelectorAll('select option[data-i18n]').forEach(option => {
            const key = option.getAttribute('data-i18n');
            const translation = this.getTranslation(key);
            if (translation) {
                option.textContent = translation;
            }
        });

        // 處理 data-content-key 屬性（動態內容）
        const contentElements = document.querySelectorAll('[data-content-key]');
        console.log('Found content elements:', contentElements.length);
        contentElements.forEach(element => {
            const key = element.getAttribute('data-content-key');
            const translation = this.getTranslation(key);
            console.log('Translating content key:', key, '→', translation ? translation.substring(0, 50) + '...' : 'NOT FOUND');
            if (translation) {
                element.textContent = translation;
            }
        });
    }

    getTranslation(key) {
        const langData = translations[this.currentLang];
        return langData ? langData[key] : key;
    }

    updateLanguageButtons() {
        const langButtons = document.querySelectorAll('[data-lang]');
        langButtons.forEach(button => {
            const lang = button.getAttribute('data-lang');
            if (lang === this.currentLang) {
                button.classList.add('active');
                button.style.fontWeight = 'bold';
            } else {
                button.classList.remove('active');
                button.style.fontWeight = 'normal';
            }
        });
    }
}

// 全域語言管理器實例
let languageManager;

// 頁面載入後初始化
document.addEventListener('DOMContentLoaded', () => {
    languageManager = new LanguageManager();
});
