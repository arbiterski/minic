// Minic 風格的神經學研究資料庫平台 - 前端應用邏輯

class MinicPortal {
    constructor() {
        this.currentFilters = {
            resourceType: ['data'],
            access: ['open'],
            sortBy: 'relevance'
        };
        this.searchTerm = '';
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadDownloadInfo();
        // this.initializeFilters(); // 註解掉未實作的函數
    }

    bindEvents() {
        // 搜尋表單
        const searchForm = document.getElementById('searchForm');
        if (searchForm) {
            searchForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.performSearch();
            });
        }

        // 篩選按鈕
        const applyFiltersBtn = document.getElementById('applyFilters');
        if (applyFiltersBtn) {
            applyFiltersBtn.addEventListener('click', () => {
                this.applyFilters();
            });
        }

        // 資源類型篩選
        document.querySelectorAll('input[type="checkbox"][id$="Check"]').forEach(checkbox => {
            checkbox.addEventListener('change', () => {
                this.updateFilterState();
            });
        });

        // 排序下拉選單
        const sortSelect = document.getElementById('sortSelect');
        if (sortSelect) {
            sortSelect.addEventListener('change', () => {
                this.currentFilters.sortBy = sortSelect.value;
            });
        }

        // 資源卡片點擊事件
        document.querySelectorAll('.resource-card').forEach(card => {
            const titleLink = card.querySelector('.resource-title a');
            if (titleLink) {
                titleLink.addEventListener('click', (e) => {
                    e.preventDefault();
                    const href = titleLink.getAttribute('href');
                    this.navigateToResource(href);
                });
            }
        });
    }

    updateFilterState() {
        // 更新資源類型篩選
        this.currentFilters.resourceType = [];
        document.querySelectorAll('input[type="checkbox"][id$="Check"]:checked').forEach(checkbox => {
            if (checkbox.id.includes('Check')) {
                this.currentFilters.resourceType.push(checkbox.value);
            }
        });

        // 更新存取權限篩選
        this.currentFilters.access = [];
        document.querySelectorAll('input[type="checkbox"][id$="Check"]:checked').forEach(checkbox => {
            if (checkbox.id.includes('open') || checkbox.id.includes('restricted')) {
                this.currentFilters.access.push(checkbox.value);
            }
        });
    }

    performSearch() {
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            this.searchTerm = searchInput.value.trim();
            if (this.searchTerm) {
                this.showLoading(`正在搜尋: ${this.searchTerm}`);
                
                // 模擬搜尋操作
                setTimeout(() => {
                    this.hideLoading();
                    this.filterResources();
                    this.showAlert(`已搜尋: ${this.searchTerm}`, 'info');
                }, 800);
            }
        }
    }

    applyFilters() {
        this.showLoading('正在套用篩選...');
        
        // 模擬篩選操作
        setTimeout(() => {
            this.hideLoading();
            this.filterResources();
            this.showAlert('篩選已套用', 'success');
        }, 500);
    }

    filterResources() {
        const resourceCards = document.querySelectorAll('.resource-card');
        
        resourceCards.forEach(card => {
            const type = card.getAttribute('data-type');
            const access = card.getAttribute('data-access');
            const title = card.querySelector('.resource-title').textContent.toLowerCase();
            const description = card.querySelector('.resource-description').textContent.toLowerCase();
            
            let shouldShow = true;
            
            // 檢查資源類型篩選
            if (this.currentFilters.resourceType.length > 0 && !this.currentFilters.resourceType.includes(type)) {
                shouldShow = false;
            }
            
            // 檢查存取權限篩選
            if (this.currentFilters.access.length > 0 && !this.currentFilters.access.includes(access)) {
                shouldShow = false;
            }
            
            // 檢查搜尋詞
            if (this.searchTerm && !title.includes(this.searchTerm.toLowerCase()) && !description.includes(this.searchTerm.toLowerCase())) {
                shouldShow = false;
            }
            
            // 顯示或隱藏資源卡片
            if (shouldShow) {
                card.style.display = 'block';
                card.classList.add('fade-in');
            } else {
                card.style.display = 'none';
                card.classList.remove('fade-in');
            }
        });
        
        // 應用排序
        this.sortResources();
    }

    sortResources() {
        const resourceContainer = document.querySelector('.resource-card').parentElement;
        const resourceCards = Array.from(document.querySelectorAll('.resource-card:not([style*="display: none"])'));
        
        resourceCards.sort((a, b) => {
            const sortBy = this.currentFilters.sortBy;
            
            switch (sortBy) {
                case 'latest':
                    return this.compareDates(a, b, 'desc');
                case 'oldest':
                    return this.compareDates(a, b, 'asc');
                case 'title_asc':
                    return this.compareTitles(a, b, 'asc');
                case 'title_desc':
                    return this.compareTitles(a, b, 'desc');
                case 'size_asc':
                    return this.compareSizes(a, b, 'asc');
                case 'size_desc':
                    return this.compareSizes(a, b, 'desc');
                default: // relevance
                    return 0;
            }
        });
        
        // 重新排列 DOM 元素
        resourceCards.forEach(card => {
            resourceContainer.appendChild(card);
        });
    }

    compareDates(a, b, order) {
        const dateA = new Date(a.querySelector('.resource-meta p:first-child').textContent.replace('發布日期: ', ''));
        const dateB = new Date(b.querySelector('.resource-meta p:first-child').textContent.replace('發布日期: ', ''));
        return order === 'asc' ? dateA - dateB : dateB - dateA;
    }

    compareTitles(a, b, order) {
        const titleA = a.querySelector('.resource-title').textContent.toLowerCase();
        const titleB = b.querySelector('.resource-title').textContent.toLowerCase();
        if (order === 'asc') {
            return titleA.localeCompare(titleB);
        } else {
            return titleB.localeCompare(titleA);
        }
    }

    compareSizes(a, b, order) {
        const sizeA = this.parseSize(a.querySelector('.resource-meta p:last-child').textContent);
        const sizeB = this.parseSize(b.querySelector('.resource-meta p:last-child').textContent);
        return order === 'asc' ? sizeA - sizeB : sizeB - sizeA;
    }

    parseSize(sizeText) {
        const match = sizeText.match(/(\d+(?:\.\d+)?)\s*(KB|MB|GB)/);
        if (match) {
            const value = parseFloat(match[1]);
            const unit = match[2];
            switch (unit) {
                case 'KB': return value;
                case 'MB': return value * 1024;
                case 'GB': return value * 1024 * 1024;
                default: return value;
            }
        }
        return 0;
    }

    navigateToResource(href) {
        this.showLoading('載入資源詳情...');
        
        // 模擬導航到資源詳情頁面
        setTimeout(() => {
            this.hideLoading();
            
            // 在實際應用中，這裡會導航到資源詳情頁面
            if (href.startsWith('/database/')) {
                window.location.href = href;
            } else if (href.startsWith('/software/')) {
                window.location.href = href;
            } else {
                this.showAlert(`正在查看資源: ${href}`, 'info');
            }
        }, 600);
    }

    async loadDownloadInfo() {
        try {
            const response = await fetch('/api/download-info');
            if (response.ok) {
                const info = await response.json();
                this.updateDownloadInfo(info);
            }
        } catch (error) {
            console.error('載入下載資訊失敗:', error);
        }
    }

    updateDownloadInfo(info) {
        const csvSizeElement = document.getElementById('csv-size');
        if (csvSizeElement && info.anonymized_csv) {
            csvSizeElement.textContent = info.anonymized_csv.size_formatted;
        }
    }

    showLoading(message) {
        const loadingMessage = document.getElementById('loadingMessage');
        if (loadingMessage) {
            loadingMessage.textContent = message;
        }
        
        const loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
        loadingModal.show();
    }

    hideLoading() {
        const loadingModal = bootstrap.Modal.getInstance(document.getElementById('loadingModal'));
        if (loadingModal) {
            loadingModal.hide();
        }
    }

    showAlert(message, type = 'info') {
        // 創建 Bootstrap alert
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.top = '20px';
        alertDiv.style.right = '20px';
        alertDiv.style.zIndex = '1050';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // 插入到頁面
        document.body.appendChild(alertDiv);
        
        // 自動消失
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 3000);
    }
}

// 頁面載入完成後初始化應用
document.addEventListener('DOMContentLoaded', () => {
    new MinicPortal();
});

// 工具函數
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('zh-TW', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// 添加 CSS 動畫類
document.addEventListener('DOMContentLoaded', () => {
    // 為資源卡片添加淡入動畫
    const resourceCards = document.querySelectorAll('.resource-card');
    resourceCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });
});
