/**
 * SAGMOTO Data Loader - 动态加载产品数据
 * 优先从localStorage加载（后台修改后的数据），否则从JSON文件加载
 */

(function() {
    const STORAGE_KEY = 'sagmoto_products_data';
    const DEFAULT_JSON_URL = 'data/products.json';

    window.SAGMOTO_DATA = {
        products: [],
        loaded: false
    };

    // 加载产品数据
    window.loadSagmotoПродукция = async function() {
        // 优先从localStorage加载（后台修改后的数据）
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) {
            try {
                const data = JSON.parse(stored);
                window.SAGMOTO_DATA.products = data.products || data;
                window.SAGMOTO_DATA.loaded = true;
                return window.SAGMOTO_DATA.products;
            } catch (e) {
                console.error('localStorage parse error:', e);
            }
        }

        // 从JSON文件加载
        try {
            const response = await fetch(DEFAULT_JSON_URL);
            const data = await response.json();
            window.SAGMOTO_DATA.products = data.products || data;
            window.SAGMOTO_DATA.loaded = true;
            return window.SAGMOTO_DATA.products;
        } catch (e) {
            console.error('Failed to load products:', e);
            window.SAGMOTO_DATA.loaded = true;
            return [];
        }
    };

    // 获取按分类分组的产品
    window.getПродукцияByКатегория = function() {
        const groups = {};
        window.SAGMOTO_DATA.products.forEach(p => {
            if (!groups[p.category]) {
                groups[p.category] = [];
            }
            groups[p.category].push(p);
        });
        return groups;
    };

    // 获取精选产品
    window.getFeaturedПродукция = function(limit = 8) {
        return window.SAGMOTO_DATA.products
            .filter(p => p.featured)
            .slice(0, limit);
    };

    // 获取分类产品（用于首页Tab，每个分类取前3个）
    window.getКатегорияПродукция = function(category, limit = 3) {
        return window.SAGMOTO_DATA.products
            .filter(p => p.category === category)
            .slice(0, limit);
    };
})();
