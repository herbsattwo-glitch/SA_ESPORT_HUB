/**
 * SA Esports Hub — Premium Animated System
 */

document.addEventListener('DOMContentLoaded', function () {

  // ════════════════════════════════════════════
  // PARTICLE NETWORK CANVAS
  // ════════════════════════════════════════════
  (function() {
    const canvas = document.getElementById('particle-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let particles = [];
    let mouse = { x: null, y: null };

    function resize() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }
    resize();

    function createParticles() {
      particles = [];
      const count = Math.min(80, Math.floor(window.innerWidth / 20));
      for (let i = 0; i < count; i++) {
        particles.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          vx: (Math.random() - 0.5) * 0.5,
          vy: (Math.random() - 0.5) * 0.5,
          r: Math.random() * 1.8 + 0.5,
          opacity: Math.random() * 0.6 + 0.2
        });
      }
    }
    createParticles();

    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      particles.forEach(p => {
        p.x += p.vx;
        p.y += p.vy;

        if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
        if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

        if (mouse.x !== null) {
          const dx = p.x - mouse.x;
          const dy = p.y - mouse.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 120) {
            const force = (120 - dist) / 120;
            p.x += (dx / dist) * force * 2;
            p.y += (dy / dist) * force * 2;
          }
        }

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(16, 124, 16, ${p.opacity})`;
        ctx.shadowBlur = 8;
        ctx.shadowColor = 'rgba(16, 124, 16, 0.5)';
        ctx.fill();
      });

      ctx.shadowBlur = 0;

      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 140) {
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.strokeStyle = `rgba(16, 124, 16, ${(1 - dist / 140) * 0.2})`;
            ctx.lineWidth = 0.8;
            ctx.stroke();
          }
        }
      }

      requestAnimationFrame(animate);
    }
    animate();

    window.addEventListener('mousemove', e => {
      mouse.x = e.clientX;
      mouse.y = e.clientY;
    });

    window.addEventListener('mouseleave', () => {
      mouse.x = null;
      mouse.y = null;
    });

    window.addEventListener('resize', () => {
      resize();
      createParticles();
    });
  })();

  // ════════════════════════════════════════════
  // SCROLL-TRIGGERED FADE-IN
  // ════════════════════════════════════════════
  const targets = document.querySelectorAll(
    '.xbox-stat-card, .xbox-player-card, .xbox-league-info-card'
  );

  if (targets.length) {
    const observer = new IntersectionObserver(
      entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
    );

    targets.forEach(el => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(20px)';
      el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      observer.observe(el);
    });
  }

  // ════════════════════════════════════════════
  // ANIMATED COUNTERS
  // ════════════════════════════════════════════
  function animateCounters() {
    document.querySelectorAll('.xbox-stat-value, .xbox-mini-stat-val').forEach(el => {
      const raw = el.textContent.trim();
      const isPercent = raw.endsWith('%');
      const target = parseFloat(raw.replace('%', ''));
      if (isNaN(target)) return;

      let current = 0;
      const duration = 1200;
      const step = 20;
      const increment = target / (duration / step);

      el.textContent = isPercent ? '0%' : '0';
      const timer = setInterval(() => {
        current += increment;
        if (current >= target) { current = target; clearInterval(timer); }
        el.textContent = isPercent
          ? Math.round(current) + '%'
          : Math.round(current).toLocaleString();
      }, step);
    });
  }

  const firstStat = document.querySelector('.xbox-stat-card, .xbox-mini-stat-val');
  if (firstStat) {
    const obs = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting) {
        animateCounters();
        obs.disconnect();
      }
    }, { threshold: 0.3 });
    obs.observe(firstStat);
  }

  // ════════════════════════════════════════════
  // RATING BAR ANIMATION
  // ════════════════════════════════════════════
  const ratingBars = document.querySelectorAll('.xbox-rating-fill');
  if (ratingBars.length) {
    const barObs = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const bar = entry.target;
          const w = bar.style.width;
          bar.style.width = '0%';
          setTimeout(() => { bar.style.width = w; }, 100);
          barObs.unobserve(bar);
        }
      });
    }, { threshold: 0.3 });
    ratingBars.forEach(b => barObs.observe(b));
  }

  // ════════════════════════════════════════════
  // RIPPLE EFFECT ON BUTTONS
  // ════════════════════════════════════════════
  document.querySelectorAll('.xbox-btn-primary, .xbox-btn-outline').forEach(btn => {
    btn.addEventListener('click', function(e) {
      const rect = this.getBoundingClientRect();
      const ripple = document.createElement('span');
      const size = Math.max(rect.width, rect.height);
      const x = e.clientX - rect.left - size / 2;
      const y = e.clientY - rect.top - size / 2;

      ripple.style.cssText = `
        position:absolute;width:${size}px;height:${size}px;
        left:${x}px;top:${y}px;
        background:rgba(255,255,255,0.25);border-radius:50%;
        transform:scale(0);animation:rippleEffect 0.6s ease-out;
        pointer-events:none;z-index:10;
      `;

      if (!document.getElementById('ripple-style')) {
        const style = document.createElement('style');
        style.id = 'ripple-style';
        style.textContent = `
          @keyframes rippleEffect {
            to { transform: scale(2.5); opacity: 0; }
          }
        `;
        document.head.appendChild(style);
      }

      this.style.position = 'relative';
      this.style.overflow = 'hidden';
      this.appendChild(ripple);
      setTimeout(() => ripple.remove(), 700);
    });
  });

  // ════════════════════════════════════════════
  // NAVBAR SCROLL EFFECT
  // ════════════════════════════════════════════
  const navbar = document.querySelector('.xbox-navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 50) {
        navbar.style.background = 'rgba(8, 8, 8, 0.85)';
        navbar.style.boxShadow = '0 4px 24px rgba(16, 124, 16, 0.15)';
      } else {
        navbar.style.background = 'rgba(15, 15, 15, 0.7)';
        navbar.style.boxShadow = 'none';
      }
    }, { passive: true });
  }

  // ════════════════════════════════════════════
  // AUTO-DISMISS ALERTS
  // ════════════════════════════════════════════
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 5000);
  });

  // ════════════════════════════════════════════
  // FILE INPUT PREVIEW
  // ════════════════════════════════════════════
  document.querySelectorAll('input[type="file"]').forEach(input => {
    input.addEventListener('change', function() {
      const file = this.files[0];
      if (!file) return;

      const existing = this.parentElement.querySelector('.xbox-img-preview');
      if (existing) existing.remove();

      const reader = new FileReader();
      reader.onload = e => {
        const img = document.createElement('img');
        img.src = e.target.result;
        img.className = 'xbox-img-preview mt-2';
        img.style.cssText = `
          max-width:160px;max-height:160px;object-fit:cover;
          border:2px solid #107C10;border-radius:10px;
          display:block;animation:cardFadeIn 0.3s ease-out;
          box-shadow:0 8px 24px rgba(16,124,16,0.3);
        `;
        input.parentElement.appendChild(img);
      };
      reader.readAsDataURL(file);
    });
  });

  console.log(
    '%c ✦ SA Esports Hub — Premium Theme ✦ ',
    'background: linear-gradient(90deg, #0E0E0E, #107C10, #0E0E0E);' +
    'color: #fff; font-weight: bold; padding: 8px 14px; border-radius: 6px;' +
    'font-family: Rajdhani, sans-serif; letter-spacing: 1px;'
  );
});