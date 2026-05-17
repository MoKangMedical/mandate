// ═══════════════ MANDATE APP LOGIC ═══════════════
'use strict';

// ═══════ Scroll-triggered fade-in ═══════
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => { if(e.isIntersecting) e.target.classList.add('visible'); });
}, {threshold:0.1});

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
  renderDynastyTimeline();
  renderDynastyFilter();
  renderEmperors();
  renderAvatarGrid();
  setupSearch();
});

// ═══════ Dynasty Timeline ═══════
function renderDynastyTimeline() {
  const track = document.getElementById('dynastyTrack');
  if(!track) return;
  track.innerHTML = DYNASTIES.map((d,i) => `
    <div class="timeline-dot ${i===0?'active':''}" onclick="filterByDynasty('${d.id}',this)" data-dynasty="${d.id}">
      <div class="bar"></div>
      <div class="era">${d.name}</div>
      <div class="years">${d.era.split('-')[0].replace('约','')}</div>
    </div>
  `).join('');
}

function filterByDynasty(dynastyId, el) {
  document.querySelectorAll('.timeline-dot').forEach(d=>d.classList.remove('active'));
  el.classList.add('active');
  document.querySelectorAll('.dynasty-pill').forEach(p=>p.classList.remove('active'));
  const pill = document.querySelector(`.dynasty-pill[data-dynasty="${dynastyId}"]`);
  if(pill) pill.classList.add('active');
  currentDynasty = dynastyId;
  document.getElementById('searchInput').value = '';
  renderEmperors();
}

let currentDynasty = 'all';

// ═══════ Dynasty Filter Pills ═══════
function renderDynastyFilter() {
  const container = document.getElementById('dynastyFilter');
  if(!container) return;
  container.innerHTML = [
    '<span class="dynasty-pill active" data-dynasty="all" onclick="setDynastyFilter(\'all\',this)">全部朝代</span>',
    ...DYNASTIES.map(d => 
      `<span class="dynasty-pill" data-dynasty="${d.id}" onclick="setDynastyFilter('${d.id}',this)">${d.name}</span>`
    )
  ].join('');
}

function setDynastyFilter(dynastyId, el) {
  document.querySelectorAll('.dynasty-pill').forEach(p=>p.classList.remove('active'));
  el.classList.add('active');
  document.querySelectorAll('.timeline-dot').forEach(d=>d.classList.remove('active'));
  if(dynastyId !== 'all') {
    const dot = document.querySelector(`.timeline-dot[data-dynasty="${dynastyId}"]`);
    if(dot) dot.classList.add('active');
  }
  currentDynasty = dynastyId;
  document.getElementById('searchInput').value = '';
  renderEmperors();
}

// ═══════ Search ═══════
function setupSearch() {
  const input = document.getElementById('searchInput');
  if(!input) return;
  input.addEventListener('input', () => {
    if(input.value.trim()) {
      currentDynasty = 'all';
      document.querySelectorAll('.dynasty-pill').forEach(p=>p.classList.remove('active'));
      document.querySelectorAll('.timeline-dot').forEach(d=>d.classList.remove('active'));
      const allBtn = document.querySelector('.dynasty-pill[data-dynasty="all"]');
      if(allBtn) allBtn.classList.add('active');
    }
    renderEmperors();
  });
}

// ═══════ Emperor Grid ═══════
function renderEmperors() {
  const grid = document.getElementById('emperorGrid');
  if(!grid) return;
  
  const query = (document.getElementById('searchInput')?.value || '').trim().toLowerCase();
  
  let filtered = EMPERORS;
  if(query) {
    filtered = EMPERORS.filter(e => 
      e.name.includes(query) || e.temple.includes(query) || e.dynasty.includes(query) ||
      e.tagline.includes(query) || e.era.includes(query) || e.tags.some(t=>t.includes(query))
    );
  } else if(currentDynasty !== 'all') {
    filtered = EMPERORS.filter(e => e.dynasty === currentDynasty);
  }
  
  if(filtered.length === 0) {
    grid.innerHTML = `<div style="grid-column:1/-1;text-align:center;padding:60px;color:var(--text3)">
      <p style="font-size:1.2rem;margin-bottom:8px">未找到匹配的帝王</p>
      <p style="font-size:0.9rem">试试其他关键词或朝代</p>
    </div>`;
    return;
  }
  
  grid.innerHTML = filtered.map(e => {
    const starsHtml = `${e.stars.toFixed(1)}/5`;
    const hasAvatar = AVATAR_SPOTLIGHT.includes(e.id);
    return `
    <div class="emperor-card" onclick="goToEmperor('${e.id}')">
      <div class="card-top">
        <div class="portrait">帝</div>
        <div class="rating">
          <div class="stars">${starsHtml}</div>
          <div class="score">${e.score}/10</div>
        </div>
      </div>
      <h3>${e.name}<span style="font-size:0.75rem;color:var(--text3);font-weight:400;margin-left:6px">${e.temple}</span></h3>
      <div class="reign">${getDynastyName(e.dynasty)} · ${e.reign}</div>
      <div class="tagline">${e.tagline}</div>
      <div class="eval-bar">
        ${renderDimBar('大一统',e.dims.unity)}
        ${renderDimBar('民生',e.dims.livelihood)}
        ${renderDimBar('制度',e.dims.system)}
        ${renderDimBar('文化',e.dims.culture)}
        ${renderDimBar('影响',e.dims.legacy)}
      </div>
      <div class="tags">
        ${e.tags.slice(0,3).map(t=>`<span class="tag${hasAvatar?' gold':''}">${t}</span>`).join('')}
      </div>
      ${hasAvatar ? `<div class="chat-badge">AI对话</div>` : ''}
    </div>`;
  }).join('');
}

function renderDimBar(label, val) {
  const cls = val >= 6 ? 'pos' : 'neg';
  return `<div class="eval-row"><span class="eval-label">${label}</span><div class="eval-track"><div class="eval-fill ${cls}" style="width:${val*10}%"></div></div></div>`;
}

function getDynastyName(id) {
  const d = DYNASTIES.find(d=>d.id===id);
  return d ? d.name : id;
}

function goToEmperor(id) {
  window.location.href = `emperor.html?id=${id}`;
}

// ═══════ Digital Avatar Grid ═══════
function renderAvatarGrid() {
  const grid = document.getElementById('avatarGrid');
  if(!grid) return;
  
  grid.innerHTML = AVATAR_SPOTLIGHT.map(id => {
    const e = EMPERORS.find(emp => emp.id === id);
    if(!e) return '';
    return `
    <div class="avatar-card" onclick="openChat('${e.id}')">
      <div class="avatar-icon">帝</div>
      <h3>${e.name}</h3>
      <div class="avatar-dynasty">${getDynastyName(e.dynasty)} · ${e.reign}</div>
      <div class="avatar-quote">「${e.avatar.quote}」</div>
      <div style="margin-top:12px;font-size:0.75rem;color:var(--red)">
        <span class="live-dot"></span>可对话
      </div>
    </div>`;
  }).join('');
}

function openChat(emperorId) {
  window.location.href = `chat.html?id=${emperorId}`;
}

// ═══════ Toast ═══════
function showToast(msg) {
  const t = document.getElementById('toast');
  if(!t) return;
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'), 2000);
}
