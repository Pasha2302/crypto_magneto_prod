/* ============================================
   Crypto Listing Website - Main JavaScript
   Pure JavaScript - No Frameworks
   ============================================ */

// ========== Data Models & API Stubs ==========

// Фиктивные данные криптовалюты
const mockCryptoData = [
    {
        id: 'bitcoin',
        rank: 1,
        name: 'Bitcoin',
        symbol: 'BTC',
        price: 43250.50,
        change24h: 2.45,
        change7d: -5.32,
        marketCap: 848750000000,
        volume24h: 28500000000,
        supply: 19600000,
        maxSupply: 21000000,
        logo: '₿'
    },
    {
        id: 'ethereum',
        rank: 2,
        name: 'Ethereum',
        symbol: 'ETH',
        price: 2650.75,
        change24h: 3.12,
        change7d: 8.45,
        marketCap: 318500000000,
        volume24h: 15200000000,
        supply: 120250000,
        maxSupply: null,
        logo: 'Ξ'
    },
    {
        id: 'binance-coin',
        rank: 3,
        name: 'Binance Coin',
        symbol: 'BNB',
        price: 315.20,
        change24h: -1.25,
        change7d: 4.32,
        marketCap: 47280000000,
        volume24h: 1250000000,
        supply: 150000000,
        maxSupply: 200000000,
        logo: 'BNB'
    },
    {
        id: 'solana',
        rank: 4,
        name: 'Solana',
        symbol: 'SOL',
        price: 98.45,
        change24h: 5.67,
        change7d: -2.15,
        marketCap: 45287000000,
        volume24h: 2100000000,
        supply: 460000000,
        maxSupply: null,
        logo: 'SOL'
    },
    {
        id: 'cardano',
        rank: 5,
        name: 'Cardano',
        symbol: 'ADA',
        price: 0.52,
        change24h: 1.89,
        change7d: 6.23,
        marketCap: 18447000000,
        volume24h: 450000000,
        supply: 35466000000,
        maxSupply: 45000000000,
        logo: 'ADA'
    },
    {
        id: 'polkadot',
        rank: 6,
        name: 'Polkadot',
        symbol: 'DOT',
        price: 7.25,
        change24h: -0.75,
        change7d: 3.45,
        marketCap: 9425000000,
        volume24h: 280000000,
        supply: 1300000000,
        maxSupply: null,
        logo: 'DOT'
    },
    {
        id: 'avalanche',
        rank: 7,
        name: 'Avalanche',
        symbol: 'AVAX',
        price: 36.80,
        change24h: 4.12,
        change7d: -1.25,
        marketCap: 13824000000,
        volume24h: 520000000,
        supply: 376000000,
        maxSupply: 720000000,
        logo: 'AVAX'
    },
    {
        id: 'chainlink',
        rank: 8,
        name: 'Chainlink',
        symbol: 'LINK',
        price: 14.65,
        change24h: 2.34,
        change7d: 7.89,
        marketCap: 8780000000,
        volume24h: 340000000,
        supply: 600000000,
        maxSupply: 1000000000,
        logo: 'LINK'
    },
    {
        id: 'uniswap',
        rank: 9,
        name: 'Uniswap',
        symbol: 'UNI',
        price: 6.75,
        change24h: -2.15,
        change7d: 5.67,
        marketCap: 4050000000,
        volume24h: 180000000,
        supply: 600000000,
        maxSupply: 1000000000,
        logo: 'UNI'
    },
    {
        id: 'litecoin',
        rank: 10,
        name: 'Litecoin',
        symbol: 'LTC',
        price: 72.30,
        change24h: 1.56,
        change7d: -3.21,
        marketCap: 5378000000,
        volume24h: 420000000,
        supply: 74400000,
        maxSupply: 84000000,
        logo: 'Ł'
    }
];

// Фиктивные поисковые данные с монетами (для раскрывающегося списка поиска)
const mockSearchData = [
    { id: 'baby-shibarium', name: 'Baby Shibarium', symbol: 'BABYSHIB', network: 'ETH', logo: '🐕' },
    { id: 'shiba-gold', name: 'Shiba Gold', symbol: 'SHIBG', network: 'BSC', logo: '🐕' },
    { id: 'space-dog-shiba', name: 'SpaceDogShiba', symbol: 'SPACEDOG', network: 'BSC', logo: '🐕' },
    { id: 'shiba-saga', name: 'ShibaSaga', symbol: 'SHIBAS', network: 'ETH', logo: '🐕' },
    { id: 'shiba-ocean', name: 'SHIBA OCEAN', symbol: 'SHIBOC', network: 'BSC', logo: '🐕' },
    { id: 'shiba-inu', name: 'Shiba Inu', symbol: 'SHIB', network: 'ETH', logo: '🐕' },
    { id: 'baby-doge', name: 'Baby Doge', symbol: 'BABYDOGE', network: 'BSC', logo: '🐕' },
    { id: 'floki', name: 'Floki', symbol: 'FLOKI', network: 'ETH', logo: '🐕' }
];

// Extended token details (for token detail page)
const tokenDetails = {
    'bitcoin': {
        description: 'Bitcoin is a decentralized digital currency that enables peer-to-peer transactions without the need for intermediaries.',
        blockchain: 'Bitcoin',
        contractAddress: 'N/A',
        tokenStandard: 'Native',
        website: 'https://bitcoin.org',
        whitepaper: 'https://bitcoin.org/bitcoin.pdf',
        twitter: 'https://twitter.com/bitcoin',
        telegram: null,
        discord: null,
        github: 'https://github.com/bitcoin',
        medium: null,
        audit: null,
        securityScore: 9.5,
        auditProvider: 'Self-Validated',
        launchDate: '2009-01-03',
        launchPrice: 0.0008,
        tokenomics: [
            { label: 'Mining Rewards', value: 100 },
        ],
        exchanges: [
            { name: 'Binance', type: 'CEX', logo: 'BNB', url: 'https://binance.com' },
            { name: 'Coinbase', type: 'CEX', logo: 'CB', url: 'https://coinbase.com' },
            { name: 'Kraken', type: 'CEX', logo: 'KR', url: 'https://kraken.com' },
        ],
        airdrop: null,
        pricePredictions: [
            { year: 2024, min: 40000, avg: 50000, max: 65000, confidence: 'High' },
            { year: 2025, min: 60000, avg: 80000, max: 100000, confidence: 'Medium' },
            { year: 2026, min: 80000, avg: 120000, max: 150000, confidence: 'Low' },
        ]
    },
    'ethereum': {
        description: 'Ethereum is a decentralized platform that enables smart contracts and decentralized applications (DApps).',
        blockchain: 'Ethereum',
        contractAddress: '0x0000000000000000000000000000000000000000',
        tokenStandard: 'Native',
        website: 'https://ethereum.org',
        whitepaper: 'https://ethereum.org/en/whitepaper/',
        twitter: 'https://twitter.com/ethereum',
        telegram: null,
        discord: 'https://discord.gg/ethereum',
        github: 'https://github.com/ethereum',
        medium: 'https://blog.ethereum.org',
        audit: 'https://ethereum.org/en/security',
        securityScore: 9.2,
        auditProvider: 'Multiple Auditors',
        launchDate: '2015-07-30',
        launchPrice: 0.311,
        tokenomics: [
            { label: 'Public Sale', value: 60 },
            { label: 'Ethereum Foundation', value: 20 },
            { label: 'Early Contributors', value: 20 },
        ],
        exchanges: [
            { name: 'Binance', type: 'CEX', logo: 'BNB', url: 'https://binance.com' },
            { name: 'Uniswap', type: 'DEX', logo: 'UNI', url: 'https://uniswap.org' },
            { name: 'Coinbase', type: 'CEX', logo: 'CB', url: 'https://coinbase.com' },
        ],
        airdrop: null,
        pricePredictions: [
            { year: 2024, min: 2500, avg: 3000, max: 3500, confidence: 'High' },
            { year: 2025, min: 3500, avg: 4500, max: 5500, confidence: 'Medium' },
            { year: 2026, min: 4500, avg: 6000, max: 8000, confidence: 'Low' },
        ]
    }
};

// Global market stats
const globalStats = {
    totalMarketCap: 1685000000000,
    totalVolume24h: 85000000000,
    btcDominance: 50.3,
    activeCryptocurrencies: 12500,
    marketCapChange24h: 2.45
};

// ========== Utility Functions ==========

function formatCurrency(value, decimals = 2) {
    if (value >= 1e12) return `$${(value / 1e12).toFixed(2)}T`;
    if (value >= 1e9) return `$${(value / 1e9).toFixed(2)}B`;
    if (value >= 1e6) return `$${(value / 1e6).toFixed(2)}M`;
    if (value >= 1e3) return `$${(value / 1e3).toFixed(2)}K`;
    return `$${value.toFixed(decimals)}`;
}

function formatNumber(value) {
    return value.toLocaleString();
}

function formatPercent(value, decimals = 2) {
    const sign = value >= 0 ? '+' : '';
    return `${sign}${value.toFixed(decimals)}%`;
}

function formatSupply(value) {
    if (value >= 1e9) return `${(value / 1e9).toFixed(2)}B`;
    if (value >= 1e6) return `${(value / 1e6).toFixed(2)}M`;
    if (value >= 1e3) return `${(value / 1e3).toFixed(2)}K`;
    return value.toString();
}

// ========== Table Management ==========

let currentSort = { column: null, direction: 'asc' };
let currentPage = 1;
let itemsPerPage = 100;
let filteredData = [...mockCryptoData];

function renderTable(data = filteredData) {
    const tbody = document.querySelector('#crypto-table tbody');
    if (!tbody) return;

    const start = (currentPage - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const pageData = data.slice(start, end);

    tbody.innerHTML = pageData.map(token => `
    <tr onclick="window.location.href='token.html?id=${token.id}'">
      <td>${token.rank}</td>
      <td>
        <div class="token-info">
          <div class="token-logo">${token.logo}</div>
          <div>
            <strong>${token.name}</strong>
            <div class="token-symbol">${token.symbol}</div>
          </div>
        </div>
      </td>
      <td>${formatCurrency(token.price)}</td>
      <td class="${token.change24h >= 0 ? 'price-positive' : 'price-negative'}">
        ${formatPercent(token.change24h)}
      </td>
      <td class="${token.change7d >= 0 ? 'price-positive' : 'price-negative'}">
        ${formatPercent(token.change7d)}
      </td>
      <td>${formatCurrency(token.marketCap)}</td>
      <td>${formatCurrency(token.volume24h)}</td>
      <td>${formatSupply(token.supply)} ${token.symbol}</td>
    </tr>
  `).join('');

    renderPagination(data.length);
}

function sortTable(column) {
    if (currentSort.column === column) {
        currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
    } else {
        currentSort.column = column;
        currentSort.direction = 'asc';
    }

    filteredData.sort((a, b) => {
        let aVal, bVal;

        switch (column) {
            case 'rank': aVal = a.rank; bVal = b.rank; break;
            case 'name': aVal = a.name; bVal = b.name; break;
            case 'price': aVal = a.price; bVal = b.price; break;
            case 'change24h': aVal = a.change24h; bVal = b.change24h; break;
            case 'change7d': aVal = a.change7d; bVal = b.change7d; break;
            case 'marketCap': aVal = a.marketCap; bVal = b.marketCap; break;
            case 'volume24h': aVal = a.volume24h; bVal = b.volume24h; break;
            default: return 0;
        }

        if (typeof aVal === 'string') {
            return currentSort.direction === 'asc'
                ? aVal.localeCompare(bVal)
                : bVal.localeCompare(aVal);
        }

        return currentSort.direction === 'asc' ? aVal - bVal : bVal - aVal;
    });

    currentPage = 1;
    renderTable();
    updateSortHeaders(column);
}

function updateSortHeaders(activeColumn) {
    document.querySelectorAll('th.sortable').forEach(th => {
        th.classList.remove('sort-asc', 'sort-desc');
        if (th.dataset.column === activeColumn) {
            th.classList.add(`sort-${currentSort.direction}`);
        }
    });
}

function renderPagination(totalItems) {
    const pagination = document.getElementById('pagination');
    const paginationText = document.getElementById('pagination-text');

    // Use total available data for display (simulating large dataset)
    const totalAvailable = 9322; // Total available cryptocurrencies

    // Update pagination text
    if (paginationText) {
        const start = totalItems === 0 ? 0 : (currentPage - 1) * itemsPerPage + 1;
        const end = Math.min(currentPage * itemsPerPage, totalItems);
        // Use filtered count for current view, but show total available
        const displayTotal = filteredData.length === mockCryptoData.length ? totalAvailable : totalItems;
        paginationText.textContent = `Showing ${start} - ${end} out of ${displayTotal}`;
    }

    if (!pagination) return;

    const totalPages = Math.ceil(totalItems / itemsPerPage);
    if (totalPages <= 1) {
        pagination.innerHTML = '';
        return;
    }

    let html = `<button onclick="goToPage(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>Previous</button>`;

    for (let i = 1; i <= totalPages; i++) {
        if (i === 1 || i === totalPages || (i >= currentPage - 2 && i <= currentPage + 2)) {
            html += `<button onclick="goToPage(${i})" class="${i === currentPage ? 'active' : ''}">${i}</button>`;
        } else if (i === currentPage - 3 || i === currentPage + 3) {
            html += `<span>...</span>`;
        }
    }

    html += `<button onclick="goToPage(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>Next</button>`;
    pagination.innerHTML = html;

    // Update rows per page selector
    const rowsSelector = document.getElementById('rows-per-page');
    if (rowsSelector) {
        rowsSelector.value = itemsPerPage;
    }
}

function changeRowsPerPage(value) {
    itemsPerPage = parseInt(value);
    currentPage = 1;
    renderTable();
}

function goToPage(page) {
    const totalPages = Math.ceil(filteredData.length / itemsPerPage);
    if (page >= 1 && page <= totalPages) {
        currentPage = page;
        renderTable();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

// ========== Search Functionality ==========

function handleSearch() {
    const searchInput = document.getElementById('search-input');
    if (!searchInput) return;

    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase().trim();

        if (query === '') {
            filteredData = [...mockCryptoData];
        } else {
            filteredData = mockCryptoData.filter(token =>
                token.name.toLowerCase().includes(query) ||
                token.symbol.toLowerCase().includes(query)
            );
        }

        currentPage = 1;
        renderTable();
    });
}

// ========== Global Metrics ==========

function renderGlobalMetrics() {
    const container = document.getElementById('global-metrics');
    if (!container) return;

    container.innerHTML = `
    <div class="metric-card">
      <div class="metric-label">Total Market Cap</div>
      <div class="metric-value">${formatCurrency(globalStats.totalMarketCap)}</div>
    </div>
    <div class="metric-card">
      <div class="metric-label">24h Volume</div>
      <div class="metric-value">${formatCurrency(globalStats.totalVolume24h)}</div>
    </div>
    <div class="metric-card">
      <div class="metric-label">BTC Dominance</div>
      <div class="metric-value">${globalStats.btcDominance}%</div>
    </div>
    <div class="metric-card">
      <div class="metric-label">Active Cryptocurrencies</div>
      <div class="metric-value">${formatNumber(globalStats.activeCryptocurrencies)}</div>
    </div>
  `;
}

// ========== Token Detail Page ==========

function getTokenIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id') || 'bitcoin';
}

function renderTokenDetail() {
    const tokenId = getTokenIdFromURL();
    const token = mockCryptoData.find(t => t.id === tokenId);
    const details = tokenDetails[tokenId] || tokenDetails['bitcoin'];

    if (!token) {
        document.body.innerHTML = '<div class="container"><h1>Token not found</h1></div>';
        return;
    }

    // Update page title
    document.title = `${token.name} (${token.symbol}) - Crypto Listing`;

    // Render token header
    const header = document.getElementById('token-header');
    if (header) {
        header.innerHTML = `
      <div class="token-header-info">
        <div class="token-header-logo">${token.logo}</div>
        <div class="token-header-text">
          <h1>${token.name} <span class="symbol">(${token.symbol})</span></h1>
          <div class="price-stats">
            <div class="price-stat">
              <span class="price-stat-label">Price</span>
              <span class="price-stat-value">${formatCurrency(token.price)}</span>
            </div>
            <div class="price-stat">
              <span class="price-stat-label">1h</span>
              <span class="price-stat-value ${token.change24h >= 0 ? 'price-positive' : 'price-negative'}">
                ${formatPercent(Math.random() * 2 - 1)}
              </span>
            </div>
            <div class="price-stat">
              <span class="price-stat-label">24h</span>
              <span class="price-stat-value ${token.change24h >= 0 ? 'price-positive' : 'price-negative'}">
                ${formatPercent(token.change24h)}
              </span>
            </div>
            <div class="price-stat">
              <span class="price-stat-label">7d</span>
              <span class="price-stat-value ${token.change7d >= 0 ? 'price-positive' : 'price-negative'}">
                ${formatPercent(token.change7d)}
              </span>
            </div>
          </div>
        </div>
      </div>
      <button class="btn btn-outline btn-icon" title="Add to Watchlist">★</button>
    `;
    }

    // Render market stats
    const marketStats = document.getElementById('market-stats');
    if (marketStats) {
        const fullyDiluted = token.maxSupply ? (token.maxSupply * token.price) : null;
        marketStats.innerHTML = `
      <div class="stats-grid">
        <div class="stat-item">
          <div class="stat-label">Market Cap</div>
          <div class="stat-value">${formatCurrency(token.marketCap)}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">24h Volume</div>
          <div class="stat-value">${formatCurrency(token.volume24h)}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">Circulating Supply</div>
          <div class="stat-value">${formatSupply(token.supply)} ${token.symbol}</div>
        </div>
        ${token.maxSupply ? `
        <div class="stat-item">
          <div class="stat-label">Max Supply</div>
          <div class="stat-value">${formatSupply(token.maxSupply)} ${token.symbol}</div>
        </div>
        ` : ''}
        ${fullyDiluted ? `
        <div class="stat-item">
          <div class="stat-label">Fully Diluted Valuation</div>
          <div class="stat-value">${formatCurrency(fullyDiluted)}</div>
        </div>
        ` : ''}
        <div class="stat-item">
          <div class="stat-label">Launch Date</div>
          <div class="stat-value">${details.launchDate || 'N/A'}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">Launch Price</div>
          <div class="stat-value">${details.launchPrice ? formatCurrency(details.launchPrice, 4) : 'N/A'}</div>
        </div>
      </div>
    `;
    }

    // Render contract info
    const contractInfo = document.getElementById('contract-info');
    if (contractInfo) {
        contractInfo.innerHTML = `
      <div class="card">
        <h3>Contract & Blockchain Info</h3>
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-label">Blockchain</div>
            <div class="stat-value">${details.blockchain}</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">Token Standard</div>
            <div class="stat-value">${details.tokenStandard}</div>
          </div>
        </div>
        ${details.contractAddress && details.contractAddress !== 'N/A' ? `
        <div style="margin-top: 1rem;">
          <div class="stat-label">Contract Address</div>
          <div style="display: flex; align-items: center; gap: 0.5rem; margin-top: 0.5rem;">
            <code style="flex: 1; padding: 0.5rem; background: var(--color-base); border-radius: var(--border-radius); font-family: monospace; font-size: 0.875rem; word-break: break-all;">
              ${details.contractAddress}
            </code>
            <button class="btn btn-outline" onclick="copyToClipboard('${details.contractAddress}')">Copy</button>
          </div>
        </div>
        ` : ''}
      </div>
    `;
    }

    // Render project links
    const projectLinks = document.getElementById('project-links');
    if (projectLinks) {
        const links = [];
        if (details.website) links.push({ label: 'Website', url: details.website, icon: '🌐' });
        if (details.whitepaper) links.push({ label: 'Whitepaper', url: details.whitepaper, icon: '📄' });
        if (details.twitter) links.push({ label: 'Twitter/X', url: details.twitter, icon: '🐦' });
        if (details.telegram) links.push({ label: 'Telegram', url: details.telegram, icon: '✈️' });
        if (details.discord) links.push({ label: 'Discord', url: details.discord, icon: '💬' });
        if (details.github) links.push({ label: 'GitHub', url: details.github, icon: '💻' });
        if (details.medium) links.push({ label: 'Medium', url: details.medium, icon: '📝' });
        if (details.audit) links.push({ label: 'Audit Report', url: details.audit, icon: '✅' });

        projectLinks.innerHTML = `
      <div class="card">
        <h3>Project Links</h3>
        <div class="links-grid">
          ${links.map(link => `
            <a href="${link.url}" target="_blank" rel="noopener noreferrer" class="link-item">
              <span>${link.icon}</span>
              <span>${link.label}</span>
            </a>
          `).join('')}
        </div>
      </div>
    `;
    }

    // Render about section
    const aboutToken = document.getElementById('about-token');
    if (aboutToken) {
        aboutToken.innerHTML = `
      <div class="card">
        <h3>About ${token.name}</h3>
        <p>${details.description}</p>
      </div>
    `;
    }

    // Render safety score
    const safetyScore = document.getElementById('safety-score');
    if (safetyScore) {
        safetyScore.innerHTML = `
      <div class="card">
        <h3>Token Safety & Audit Score</h3>
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-label">Security Score</div>
            <div class="stat-value" style="font-size: 2rem; color: var(--color-primary);">${details.securityScore}/10</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">Audit Provider</div>
            <div class="stat-value">${details.auditProvider}</div>
          </div>
        </div>
      </div>
    `;
    }

    // Render exchanges
    const whereToBuy = document.getElementById('where-to-buy');
    if (whereToBuy) {
        whereToBuy.innerHTML = `
      <div class="card">
        <h3>Where to Buy</h3>
        <div class="exchange-list">
          ${details.exchanges.map(exchange => `
            <div class="exchange-item">
              <div class="exchange-info">
                <div class="exchange-logo">${exchange.logo}</div>
                <div>
                  <div><strong>${exchange.name}</strong></div>
                  <div style="font-size: 0.875rem; color: var(--color-text-secondary);">
                    <span class="badge ${exchange.type === 'CEX' ? 'badge-info' : 'badge-success'}">${exchange.type}</span>
                  </div>
                </div>
              </div>
              <a href="${exchange.url}" target="_blank" rel="noopener noreferrer" class="btn btn-primary">Trade</a>
            </div>
          `).join('')}
        </div>
      </div>
    `;
    }

    // Render tokenomics
    const tokenomics = document.getElementById('tokenomics');
    if (tokenomics) {
        tokenomics.innerHTML = `
      <div class="card">
        <h3>Tokenomics</h3>
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-label">Total Supply</div>
            <div class="stat-value">${formatSupply(token.maxSupply || token.supply)} ${token.symbol}</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">Circulating Supply</div>
            <div class="stat-value">${formatSupply(token.supply)} ${token.symbol}</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">Max Supply</div>
            <div class="stat-value">${token.maxSupply ? formatSupply(token.maxSupply) + ' ' + token.symbol : 'Unlimited'}</div>
          </div>
        </div>
        ${details.tokenomics && details.tokenomics.length > 0 ? `
        <div class="tokenomics-chart">
          <canvas id="tokenomics-chart" width="300" height="300"></canvas>
        </div>
        ` : ''}
      </div>
    `;

        // Draw tokenomics chart if available
        if (details.tokenomics && details.tokenomics.length > 0) {
            setTimeout(() => drawTokenomicsChart(details.tokenomics), 100);
        }
    }

    // Render converter
    const converter = document.getElementById('converter');
    if (converter) {
        converter.innerHTML = `
      <div class="card">
        <h3>Coin Converter</h3>
        <div class="converter">
          <div class="converter-input-group">
            <input type="number" id="convert-from" class="form-input" value="1" oninput="updateConverter()" step="0.00000001">
            <select id="convert-from-currency" class="form-select" onchange="updateConverter()">
              <option value="${token.symbol}">${token.symbol}</option>
              <option value="USD">USD</option>
              <option value="BTC">BTC</option>
              <option value="ETH">ETH</option>
            </select>
          </div>
          <button class="converter-swap" onclick="swapConverter()">⇄</button>
          <div class="converter-input-group">
            <input type="number" id="convert-to" class="form-input" readonly>
            <select id="convert-to-currency" class="form-select" onchange="updateConverter()">
              <option value="USD">USD</option>
              <option value="BTC">BTC</option>
              <option value="ETH">ETH</option>
              <option value="${token.symbol}">${token.symbol}</option>
            </select>
          </div>
        </div>
      </div>
    `;
        // Initialize converter with default value
        setTimeout(updateConverter, 100);
    }

    // Render price predictions
    const pricePredictions = document.getElementById('price-predictions');
    if (pricePredictions && details.pricePredictions) {
        pricePredictions.innerHTML = `
      <div class="card">
        <h3>Price Prediction Table</h3>
        <p style="font-size: 0.875rem; color: var(--color-text-secondary); margin-bottom: 1rem;">
          <strong>Disclaimer:</strong> These predictions are for informational purposes only and should not be considered financial advice.
        </p>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Year</th>
                <th>Min Price</th>
                <th>Avg Price</th>
                <th>Max Price</th>
                <th>Confidence</th>
              </tr>
            </thead>
            <tbody>
              ${details.pricePredictions.map(pred => `
                <tr>
                  <td>${pred.year}</td>
                  <td>${formatCurrency(pred.min)}</td>
                  <td>${formatCurrency(pred.avg)}</td>
                  <td>${formatCurrency(pred.max)}</td>
                  <td>
                    <span class="badge ${pred.confidence === 'High' ? 'badge-success' :
                pred.confidence === 'Medium' ? 'badge-warning' :
                    'badge-danger'
            }">${pred.confidence}</span>
                  </td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
    }

    // Render airdrop
    const airdrop = document.getElementById('airdrop');
    if (airdrop) {
        if (details.airdrop) {
            airdrop.innerHTML = `
        <div class="airdrop-card">
          <h3>${details.airdrop.title}</h3>
          <p>${details.airdrop.description}</p>
          <div style="margin: 1rem 0;">
            <span class="badge badge-success">${details.airdrop.status}</span>
          </div>
          <a href="${details.airdrop.url}" target="_blank" rel="noopener noreferrer" class="btn btn-primary">Participate</a>
        </div>
      `;
        } else {
            airdrop.innerHTML = '';
        }
    }

    // Render FAQ
    const faq = document.getElementById('faq');
    if (faq) {
        faq.innerHTML = `
      <div class="card">
        <h3>Frequently Asked Questions</h3>
        <div class="accordion">
          <div class="accordion-item">
            <div class="accordion-header" onclick="toggleAccordion(this)">
              <span>What is ${token.name}?</span>
              <span class="accordion-icon">▼</span>
            </div>
            <div class="accordion-content">
              <p>${details.description}</p>
            </div>
          </div>
          <div class="accordion-item">
            <div class="accordion-header" onclick="toggleAccordion(this)">
              <span>How to buy ${token.symbol}?</span>
              <span class="accordion-icon">▼</span>
            </div>
            <div class="accordion-content">
              <p>You can purchase ${token.symbol} on various exchanges. Visit the "Where to Buy" section above to see available exchanges. Always do your own research (DYOR) before making any purchase.</p>
            </div>
          </div>
          <div class="accordion-item">
            <div class="accordion-header" onclick="toggleAccordion(this)">
              <span>Is ${token.symbol} audited?</span>
              <span class="accordion-icon">▼</span>
            </div>
            <div class="accordion-content">
              <p>${token.symbol} has a security score of ${details.securityScore}/10. ${details.auditProvider ? `Audit provided by ${details.auditProvider}.` : 'For more details, check the audit report in the Project Links section.'}</p>
            </div>
          </div>
          <div class="accordion-item">
            <div class="accordion-header" onclick="toggleAccordion(this)">
              <span>What are the contract details?</span>
              <span class="accordion-icon">▼</span>
            </div>
            <div class="accordion-content">
              <p>Blockchain: ${details.blockchain}<br>Token Standard: ${details.tokenStandard}${details.contractAddress && details.contractAddress !== 'N/A' ? `<br>Contract Address: ${details.contractAddress}` : ''}</p>
            </div>
          </div>
          <div class="accordion-item">
            <div class="accordion-header" onclick="toggleAccordion(this)">
              <span>Is ${token.symbol} a safe investment?</span>
              <span class="accordion-icon">▼</span>
            </div>
            <div class="accordion-content">
              <p><strong>Disclaimer:</strong> This is not financial advice. Cryptocurrency investments carry inherent risks. Always conduct thorough research, only invest what you can afford to lose, and consider consulting with a financial advisor.</p>
            </div>
          </div>
        </div>
      </div>
    `;
    }

    // Initialize chart
    initializeChart();
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert('Copied to clipboard!');
    }).catch(() => {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        alert('Copied to clipboard!');
    });
}

function drawTokenomicsChart(data) {
    const canvas = document.getElementById('tokenomics-chart');
    if (!canvas) return;

    // Ensure canvas has proper size
    const container = canvas.parentElement;
    if (container) {
        const size = Math.min(container.clientWidth || 300, container.clientHeight || 300);
        canvas.width = size;
        canvas.height = size;
    }

    const ctx = canvas.getContext('2d');
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = Math.min(centerX, centerY) - 20;

    let currentAngle = -Math.PI / 2;
    const total = data.reduce((sum, item) => sum + item.value, 0);

    const colors = ['#4D93F8', '#2A51C1', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'];

    data.forEach((item, index) => {
        const sliceAngle = (item.value / total) * 2 * Math.PI;

        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle);
        ctx.closePath();
        ctx.fillStyle = colors[index % colors.length];
        ctx.fill();

        // Draw label
        const labelAngle = currentAngle + sliceAngle / 2;
        const labelX = centerX + Math.cos(labelAngle) * (radius * 0.7);
        const labelY = centerY + Math.sin(labelAngle) * (radius * 0.7);

        ctx.fillStyle = 'white';
        ctx.font = '12px Inter';
        ctx.textAlign = 'center';
        ctx.fillText(`${item.label}: ${item.value}%`, labelX, labelY);

        currentAngle += sliceAngle;
    });
}

let currentChartPeriod = '24h';

function initializeChart() {
    const chartContainer = document.getElementById('chart-container');
    if (!chartContainer) return;

    chartContainer.innerHTML = `
    <div class="card">
      <div class="card-header">
        <h3 class="card-title">Price Chart</h3>
      </div>
      <div class="chart-controls">
        <button class="chart-btn ${currentChartPeriod === '24h' ? 'active' : ''}" onclick="switchChartPeriod('24h')">24h</button>
        <button class="chart-btn ${currentChartPeriod === '7d' ? 'active' : ''}" onclick="switchChartPeriod('7d')">7d</button>
        <button class="chart-btn ${currentChartPeriod === '30d' ? 'active' : ''}" onclick="switchChartPeriod('30d')">30d</button>
        <button class="chart-btn ${currentChartPeriod === '1y' ? 'active' : ''}" onclick="switchChartPeriod('1y')">1y</button>
      </div>
      <div class="chart-container">
        <canvas id="price-chart"></canvas>
      </div>
    </div>
  `;

    // Set canvas size based on container
    const canvas = document.getElementById('price-chart');
    if (canvas) {
        const container = canvas.parentElement;
        canvas.width = container.clientWidth || 800;
        canvas.height = 300;
    }

    drawChart(currentChartPeriod);

    // Handle window resize
    window.addEventListener('resize', () => {
        const canvas = document.getElementById('price-chart');
        if (canvas) {
            const container = canvas.parentElement;
            canvas.width = container.clientWidth || 800;
            canvas.height = 300;
            drawChart(currentChartPeriod);
        }
    });
}

function switchChartPeriod(period) {
    currentChartPeriod = period;
    document.querySelectorAll('.chart-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.textContent.trim() === period) {
            btn.classList.add('active');
        }
    });
    drawChart(period);
}

function drawChart(period) {
    const canvas = document.getElementById('price-chart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const tokenId = getTokenIdFromURL();
    const token = mockCryptoData.find(t => t.id === tokenId) || mockCryptoData[0];

    // Generate mock price data
    const points = 50;
    const data = [];
    const basePrice = token.price;

    for (let i = 0; i < points; i++) {
        const variation = (Math.random() - 0.5) * 0.1;
        data.push(basePrice * (1 + variation * (i / points)));
    }

    const width = canvas.width;
    const height = canvas.height;
    const padding = 40;
    const chartWidth = width - padding * 2;
    const chartHeight = height - padding * 2;

    ctx.clearRect(0, 0, width, height);

    // Draw grid
    ctx.strokeStyle = '#E5E7EB';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 5; i++) {
        const y = padding + (chartHeight / 5) * i;
        ctx.beginPath();
        ctx.moveTo(padding, y);
        ctx.lineTo(width - padding, y);
        ctx.stroke();
    }

    // Draw price line
    const minPrice = Math.min(...data);
    const maxPrice = Math.max(...data);
    const priceRange = maxPrice - minPrice || 1;

    ctx.strokeStyle = '#4D93F8';
    ctx.lineWidth = 2;
    ctx.beginPath();

    data.forEach((price, index) => {
        const x = padding + (chartWidth / (points - 1)) * index;
        const y = padding + chartHeight - ((price - minPrice) / priceRange) * chartHeight;

        if (index === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });

    ctx.stroke();

    // Fill area under line
    ctx.fillStyle = 'rgba(77, 147, 248, 0.1)';
    ctx.lineTo(width - padding, height - padding);
    ctx.lineTo(padding, height - padding);
    ctx.closePath();
    ctx.fill();

    // Draw labels
    ctx.fillStyle = '#6B7280';
    ctx.font = '12px Inter';
    ctx.textAlign = 'center';
    ctx.fillText(formatCurrency(minPrice), padding / 2, height - padding);
    ctx.fillText(formatCurrency(maxPrice), padding / 2, padding + 5);
}

function updateConverter() {
    const fromInput = document.getElementById('convert-from');
    const fromCurrency = document.getElementById('convert-from-currency').value;
    const toCurrency = document.getElementById('convert-to-currency').value;
    const toInput = document.getElementById('convert-to');

    if (!fromInput || !toInput) return;

    const tokenId = getTokenIdFromURL();
    const token = mockCryptoData.find(t => t.id === tokenId) || mockCryptoData[0];
    const btcPrice = mockCryptoData.find(t => t.symbol === 'BTC')?.price || 43250;
    const ethPrice = mockCryptoData.find(t => t.symbol === 'ETH')?.price || 2650;

    let fromValue = parseFloat(fromInput.value) || 0;
    let result = 0;

    // Convert from to USD
    if (fromCurrency === token.symbol) {
        fromValue = fromValue * token.price;
    } else if (fromCurrency === 'BTC') {
        fromValue = fromValue * btcPrice;
    } else if (fromCurrency === 'ETH') {
        fromValue = fromValue * ethPrice;
    }

    // Convert USD to toCurrency
    if (toCurrency === token.symbol) {
        result = fromValue / token.price;
    } else if (toCurrency === 'BTC') {
        result = fromValue / btcPrice;
    } else if (toCurrency === 'ETH') {
        result = fromValue / ethPrice;
    } else {
        result = fromValue;
    }

    toInput.value = result.toFixed(8);
}

function swapConverter() {
    const fromCurrency = document.getElementById('convert-from-currency');
    const toCurrency = document.getElementById('convert-to-currency');

    if (!fromCurrency || !toCurrency) return;

    const temp = fromCurrency.value;
    fromCurrency.value = toCurrency.value;
    toCurrency.value = temp;

    updateConverter();
}

function toggleAccordion(header) {
    const item = header.parentElement;
    const isActive = item.classList.contains('active');

    document.querySelectorAll('.accordion-item').forEach(i => {
        i.classList.remove('active');
    });

    if (!isActive) {
        item.classList.add('active');
    }
}

// ========== Analytics Page ==========

function renderAnalytics() {
    // Global market cap chart
    drawMarketCapChart();

    // Dominance pie chart
    drawDominanceChart();

    // Gainers/Losers
    renderGainersLosers();
}

function drawMarketCapChart() {
    const canvas = document.getElementById('market-cap-chart');
    if (!canvas) return;

    // Ensure canvas has proper size
    const container = canvas.parentElement;
    if (container) {
        canvas.width = container.clientWidth || 800;
        canvas.height = container.clientHeight || 400;
    }

    const ctx = canvas.getContext('2d');
    const data = [
        { month: 'Jan', value: 1620000000000 },
        { month: 'Feb', value: 1650000000000 },
        { month: 'Mar', value: 1680000000000 },
        { month: 'Apr', value: 1670000000000 },
        { month: 'May', value: 1690000000000 },
        { month: 'Jun', value: 1685000000000 },
    ];

    const width = canvas.width;
    const height = canvas.height;
    const padding = 40;
    const chartWidth = width - padding * 2;
    const chartHeight = height - padding * 2;

    ctx.clearRect(0, 0, width, height);

    const maxValue = Math.max(...data.map(d => d.value));
    const minValue = Math.min(...data.map(d => d.value));
    const range = maxValue - minValue || 1;

    // Draw bars
    const barWidth = chartWidth / data.length - 10;
    data.forEach((item, index) => {
        const barHeight = ((item.value - minValue) / range) * chartHeight;
        const x = padding + (chartWidth / data.length) * index + 5;
        const y = height - padding - barHeight;

        ctx.fillStyle = '#4D93F8';
        ctx.fillRect(x, y, barWidth, barHeight);

        ctx.fillStyle = '#6B7280';
        ctx.font = '10px Inter';
        ctx.textAlign = 'center';
        ctx.fillText(item.month, x + barWidth / 2, height - padding + 15);
    });

    ctx.fillStyle = '#6B7280';
    ctx.font = '12px Inter';
    ctx.textAlign = 'right';
    ctx.fillText(formatCurrency(minValue), padding - 10, height - padding);
    ctx.fillText(formatCurrency(maxValue), padding - 10, padding + 5);
}

function drawDominanceChart() {
    const canvas = document.getElementById('dominance-chart');
    if (!canvas) return;

    // Ensure canvas has proper size
    const container = canvas.parentElement;
    if (container) {
        const size = Math.min(container.clientWidth || 400, container.clientHeight || 400);
        canvas.width = size;
        canvas.height = size;
    }

    const ctx = canvas.getContext('2d');
    const data = [
        { label: 'Bitcoin', value: 50.3 },
        { label: 'Ethereum', value: 18.9 },
        { label: 'Others', value: 30.8 },
    ];

    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = Math.min(centerX, centerY) - 20;

    let currentAngle = -Math.PI / 2;
    const total = 100;

    const colors = ['#4D93F8', '#2A51C1', '#10B981'];

    data.forEach((item, index) => {
        const sliceAngle = (item.value / total) * 2 * Math.PI;

        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle);
        ctx.closePath();
        ctx.fillStyle = colors[index % colors.length];
        ctx.fill();

        const labelAngle = currentAngle + sliceAngle / 2;
        const labelX = centerX + Math.cos(labelAngle) * (radius * 0.6);
        const labelY = centerY + Math.sin(labelAngle) * (radius * 0.6);

        ctx.fillStyle = 'white';
        ctx.font = 'bold 14px Inter';
        ctx.textAlign = 'center';
        ctx.fillText(`${item.value}%`, labelX, labelY);

        currentAngle += sliceAngle;
    });

    // Draw legend
    let legendY = 20;
    data.forEach((item, index) => {
        ctx.fillStyle = colors[index];
        ctx.fillRect(20, legendY, 15, 15);
        ctx.fillStyle = '#111827';
        ctx.font = '12px Inter';
        ctx.textAlign = 'left';
        ctx.fillText(item.label, 40, legendY + 12);
        legendY += 20;
    });
}

function renderGainersLosers() {
    const gainersContainer = document.getElementById('top-gainers');
    const losersContainer = document.getElementById('top-losers');

    const sorted = [...mockCryptoData].sort((a, b) => b.change24h - a.change24h);
    const gainers = sorted.slice(0, 5);
    const losers = sorted.slice(-5).reverse();

    if (gainersContainer) {
        gainersContainer.innerHTML = `
      <div class="card">
        <h3>Top Gainers (24h)</h3>
        <div class="exchange-list">
          ${gainers.map(token => `
            <div class="exchange-item" onclick="window.location.href='token.html?id=${token.id}'">
              <div class="exchange-info">
                <div class="exchange-logo">${token.logo}</div>
                <div>
                  <div><strong>${token.name}</strong></div>
                  <div style="font-size: 0.875rem; color: var(--color-text-secondary);">${token.symbol}</div>
                </div>
              </div>
              <div class="price-positive" style="font-weight: 600;">${formatPercent(token.change24h)}</div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
    }

    if (losersContainer) {
        losersContainer.innerHTML = `
      <div class="card">
        <h3>Top Losers (24h)</h3>
        <div class="exchange-list">
          ${losers.map(token => `
            <div class="exchange-item" onclick="window.location.href='token.html?id=${token.id}'">
              <div class="exchange-info">
                <div class="exchange-logo">${token.logo}</div>
                <div>
                  <div><strong>${token.name}</strong></div>
                  <div style="font-size: 0.875rem; color: var(--color-text-secondary);">${token.symbol}</div>
                </div>
              </div>
              <div class="price-negative" style="font-weight: 600;">${formatPercent(token.change24h)}</div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
    }
}

// ========== Form Handlers ==========

function handleContactForms() {
    const listTokenForm = document.getElementById('list-token-form');
    const contactForm = document.getElementById('contact-form');

    if (listTokenForm) {
        listTokenForm.addEventListener('submit', (e) => {
            e.preventDefault();
            alert('Thank you for your submission! We will review your token listing request and get back to you shortly.');
            listTokenForm.reset();
        });
    }

    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            alert('Thank you for contacting us! We will get back to you as soon as possible.');
            contactForm.reset();
        });
    }
}

// ========== Mobile Menu ==========

function initMobileMenu() {
    const toggle = document.getElementById('mobile-menu-toggle');
    const submenuNav = document.getElementById('submenu-nav');

    if (toggle && submenuNav) {
        toggle.addEventListener('click', () => {
            const isActive = toggle.classList.toggle('active');
            submenuNav.classList.toggle('active');

            // Lock/unlock body scroll
            if (isActive) {
                document.body.style.overflow = 'hidden';
                document.body.style.position = 'fixed';
                document.body.style.width = '100%';
            } else {
                document.body.style.overflow = '';
                document.body.style.position = '';
                document.body.style.width = '';
            }
        });
    }
}

// ========== Cards Scroll Centering ==========
function initCardsScroll() {
    const contentCards = document.querySelector('.content-cards');
    if (contentCards && window.innerWidth <= 768) {
        // Center the second card (Most Viewed) on page load (mobile only)
        const secondCard = contentCards.children[1];
        if (secondCard) {
            const cardWidth = secondCard.offsetWidth;
            const cardLeft = secondCard.offsetLeft;
            const containerWidth = contentCards.offsetWidth;
            const scrollPosition = cardLeft - (containerWidth / 2) + (cardWidth / 2);
            contentCards.scrollLeft = scrollPosition;
        }
    }
}

// ========== Search Toggle ========== //
function initSearchToggle() {
    const searchToggle = document.getElementById('search-toggle');
    const searchWrapper = document.getElementById('header-search-wrapper');
    const searchClose = document.getElementById('search-close');
    const searchInput = document.getElementById('search-input');

    // Mobile search toggle
    if (searchToggle && searchWrapper) {
        searchToggle.addEventListener('click', () => {
            searchWrapper.classList.add('active');
            // Фокусируйтесь на вводе поиска после небольшой задержки, чтобы разрешить анимацию
            setTimeout(() => {
                if (searchInput) {
                    searchInput.focus();
                }
            }, 100);
        });

        // Закрыть по кнопке закрытия
        if (searchClose) {
            searchClose.addEventListener('click', () => {
                searchWrapper.classList.remove('active');
                if (searchInput) {
                    searchInput.value = '';
                    searchInput.blur();
                }
            });
        }

        // Закрыть по клику вне области поиска
        document.addEventListener('click', (e) => {
            if (searchWrapper.classList.contains('active') &&
                !searchWrapper.contains(e.target) &&
                !searchToggle.contains(e.target)) {
                searchWrapper.classList.remove('active');
                if (searchInput) {
                    searchInput.value = '';
                    searchInput.blur();
                }
            }
        });

        // Close search on Escape key
        if (searchInput) {
            searchInput.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    searchWrapper.classList.remove('active');
                    searchInput.value = '';
                    searchInput.blur();
                }
            });
        }
    }
}

// ========== Shared Search Function ==========
function performSearch(query, resultsContainer, dropdown) {
    const trimmedQuery = query.trim().toLowerCase();

    if (trimmedQuery.length === 0) {
        if (dropdown) dropdown.classList.remove('active');
        return;
    }

    // Фильтрация результатов — поиск по имени, символу или сети
    const filtered = mockSearchData.filter(coin =>
        coin.name.toLowerCase().includes(trimmedQuery) ||
        coin.symbol.toLowerCase().includes(trimmedQuery) ||
        coin.network.toLowerCase().includes(trimmedQuery)
    );

    // Также ищите в основных криптографических данных
    const mainDataFiltered = mockCryptoData.filter(coin =>
        coin.name.toLowerCase().includes(trimmedQuery) ||
        coin.symbol.toLowerCase().includes(trimmedQuery)
    ).map(coin => ({
        id: coin.id,
        name: coin.name,
        symbol: coin.symbol,
        network: coin.symbol === 'BTC' ? 'BTC' : coin.symbol === 'ETH' ? 'ETH' : 'BSC',
        logo: coin.logo
    }));

    const allResults = [...filtered, ...mainDataFiltered].slice(0, 10); // Limit to 10 results

    // Render results
    if (allResults.length > 0) {
        resultsContainer.innerHTML = allResults.map(coin => `
      <div class="search-result-item" onclick="window.location.href='token.html?id=${coin.id}'">
        <div class="search-result-icon">${coin.logo || '💰'}</div>
        <div class="search-result-info">
          <div class="search-result-name">${coin.name}</div>
        </div>
        <div class="search-result-network">${coin.network}</div>
      </div>
    `).join('');
        if (dropdown) dropdown.classList.add('active');
    } else {
        resultsContainer.innerHTML = '<div class="search-result-empty">No results found</div>';
        if (dropdown) dropdown.classList.add('active');
    }
}

// ========== Desktop Search Dropdown ==========
function initDesktopSearchDropdown() {
    const searchInput = document.getElementById('search-input-desktop');
    const dropdown = document.getElementById('search-dropdown-desktop');
    const resultsContainer = document.getElementById('search-results-desktop');
    const searchWrapper = searchInput?.closest('.header-search-wrapper');

    if (!searchInput || !dropdown || !resultsContainer) return;

    // Handle input events
    searchInput.addEventListener('input', (e) => {
        performSearch(e.target.value, resultsContainer, dropdown);
    });

    // Handle focus
    searchInput.addEventListener('focus', (e) => {
        if (e.target.value.trim().length > 0) {
            performSearch(e.target.value, resultsContainer, dropdown);
        }
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (searchWrapper && !searchWrapper.contains(e.target)) {
            dropdown.classList.remove('active');
        }
    });

    // Close dropdown on Escape key
    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            dropdown.classList.remove('active');
            searchInput.blur();
        }
    });
}

// ========== Mobile Search Dropdown ==========
function initMobileSearchDropdown() {
    const searchInput = document.getElementById('search-input');
    const dropdown = document.getElementById('search-dropdown-mobile');
    const resultsContainer = document.getElementById('search-results-mobile');
    const searchWrapper = document.getElementById('header-search-wrapper');
    const searchClose = document.getElementById('search-close');

    if (!searchInput || !dropdown || !resultsContainer || !searchWrapper) return;

    // Handle input events
    searchInput.addEventListener('input', (e) => {
        performSearch(e.target.value, resultsContainer, dropdown);
    });

    // Handle focus
    searchInput.addEventListener('focus', (e) => {
        if (e.target.value.trim().length > 0) {
            performSearch(e.target.value, resultsContainer, dropdown);
        }
    });

    // Close dropdown when search wrapper is closed
    if (searchClose) {
        searchClose.addEventListener('click', () => {
            dropdown.classList.remove('active');
            if (resultsContainer) {
                resultsContainer.innerHTML = '';
            }
        });
    }

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (searchWrapper && !searchWrapper.contains(e.target) &&
            !document.getElementById('search-toggle')?.contains(e.target)) {
            dropdown.classList.remove('active');
        }
    });

    // Close dropdown on Escape key
    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            dropdown.classList.remove('active');
        }
    });

    // Закройте раскрывающееся меню, когда оболочка поиска скрыта
    const observer = new MutationObserver(() => {
        if (!searchWrapper.classList.contains('active')) {
            dropdown.classList.remove('active');
        }
    });

    observer.observe(searchWrapper, {
        attributes: true,
        attributeFilter: ['class']
    });
}

// ========== Make functions globally accessible ==========

// Make functions available globally for inline event handlers
window.sortTable = sortTable;
window.goToPage = goToPage;
window.switchChartPeriod = switchChartPeriod;
window.updateConverter = updateConverter;
window.swapConverter = swapConverter;
window.toggleAccordion = toggleAccordion;
window.copyToClipboard = copyToClipboard;
window.changeRowsPerPage = changeRowsPerPage;

// ========== Text Block Chart ==========

function drawTextBlockChart() {
    const canvas = document.getElementById('chart-canvas');
    if (!canvas) return;

    const container = canvas.parentElement;
    const containerWidth = container.clientWidth;
    const containerHeight = container.clientHeight;

    // Set canvas size to match container
    canvas.width = containerWidth - 48; // Account for padding
    canvas.height = containerHeight - 48;

    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    // Clear canvas
    ctx.clearRect(0, 0, width, height);

    // Background grid
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
    ctx.lineWidth = 1;

    // Draw horizontal grid lines
    for (let i = 0; i <= 5; i++) {
        const y = (height / 5) * i;
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
    }

    // Draw vertical grid lines
    for (let i = 0; i <= 4; i++) {
        const x = (width / 4) * i;
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
        ctx.stroke();
    }

    // Data points (upward trend) - scaled to canvas
    const padding = 40;
    const chartWidth = width - (padding * 2);
    const chartHeight = height - (padding * 2);
    const points = [
        { x: padding + chartWidth * 0.1, y: padding + chartHeight * 0.8 },
        { x: padding + chartWidth * 0.3, y: padding + chartHeight * 0.6 },
        { x: padding + chartWidth * 0.5, y: padding + chartHeight * 0.5 },
        { x: padding + chartWidth * 0.7, y: padding + chartHeight * 0.3 },
        { x: padding + chartWidth * 0.9, y: padding + chartHeight * 0.15 }
    ];

    // Draw gradient line
    const gradient = ctx.createLinearGradient(0, height, width, 0);
    gradient.addColorStop(0, '#00F5A0'); // Green
    gradient.addColorStop(1, '#F59E0B'); // Yellow/Orange

    ctx.strokeStyle = gradient;
    ctx.lineWidth = 3;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    ctx.beginPath();
    ctx.moveTo(points[0].x, points[0].y);
    for (let i = 1; i < points.length; i++) {
        ctx.lineTo(points[i].x, points[i].y);
    }
    ctx.stroke();

    // Draw circular markers
    points.forEach(point => {
        ctx.fillStyle = '#F59E0B';
        ctx.beginPath();
        ctx.arc(point.x, point.y, 5, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#0A0B14';
        ctx.lineWidth = 2;
        ctx.stroke();
    });

    // Draw upward arrow at the end
    const lastPoint = points[points.length - 1];
    ctx.fillStyle = '#F59E0B';
    ctx.beginPath();
    ctx.moveTo(lastPoint.x, lastPoint.y - 15);
    ctx.lineTo(lastPoint.x - 8, lastPoint.y - 5);
    ctx.lineTo(lastPoint.x + 8, lastPoint.y - 5);
    ctx.closePath();
    ctx.fill();
}

// ========== Initialize ==========

document.addEventListener('DOMContentLoaded', () => {
    // Check which page we're on
    const path = window.location.pathname;
    const hash = window.location.hash;

    // Home page
    if (document.getElementById('crypto-table')) {
        renderGlobalMetrics();
        renderTable();
        handleSearch();
    }

    // Token detail page
    if (document.getElementById('token-header')) {
        renderTokenDetail();
    }

    // Analytics page
    if (document.getElementById('market-cap-chart')) {
        renderAnalytics();
    }

    // Contact page
    if (document.getElementById('list-token-form') || document.getElementById('contact-form')) {
        handleContactForms();
    }


    initMobileMenu();
    initSearchToggle();
    initDesktopSearchDropdown();
    initMobileSearchDropdown();
    initCardsScroll();

    // Set current year in footer copyright
    const currentYearElement = document.getElementById('current-year');
    if (currentYearElement) {
        currentYearElement.textContent = new Date().getFullYear();
    }
});

