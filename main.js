/**
 * 丝滑 marquee：无缝循环横向滚动 + hover 缓动减速到停 + 离开缓动恢复。
 * - 使用 requestAnimationFrame
 * - 使用时间常数的指数平滑（与帧率无关）
 * - transform: translate3d 走 GPU 合成
 */

function clamp(v, min, max) {
  return Math.max(min, Math.min(max, v));
}

function expSmoothingAlpha(dt, smoothness) {
  // smoothness: 1/s，越大越快贴近目标（与帧率无关）
  const k = Math.max(0, smoothness);
  return 1 - Math.exp(-k * dt);
}

function springStep(state, target, dt, freqHz, damping) {
  // 速度弹簧（1D）：让数值贴近 target 的同时更“自然”
  // state: { x, v } 这里我们用来控制 speed（x=当前 speed, v=加速度积分出来的速度变化率）
  const f = Math.max(0.001, freqHz);
  const z = clamp(damping, 0.05, 2.0);
  const w = 2 * Math.PI * f;

  const x = state.x;
  const v = state.v;
  const dx = x - target;

  // 经典二阶系统：x'' + 2ζω x' + ω^2 x = ω^2 target
  const a = -2 * z * w * v - (w * w) * dx;
  const v2 = v + a * dt;
  const x2 = x + v2 * dt;
  state.x = x2;
  state.v = v2;
  return state;
}

function setupMarquee(root) {
  const track = root.querySelector("[data-marquee-track]");
  if (!track) return;

  // 参数（你可以按需求调）
  const baseSpeedPxPerSec = 150; // 初始速度（px/s）
  const hoverStopSeconds = 0.55; // 悬停到停的大致时间感
  const resumeSeconds = 0.65; // 离开恢复到初速的大致时间感

  // 弹簧参数：频率越高越“跟手”，阻尼越大越不回弹
  const speedSpringHz = 3.0;
  const speedDamping = 1.05; // 1 附近接近临界阻尼

  const prefersReduced =
    window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // 无缝循环：复制一份内容
  // 注意：复制后宽度 = 原宽度 * 2，循环阈值 = 原宽度
  const originalHTML = track.innerHTML;
  track.insertAdjacentHTML("beforeend", originalHTML);

  let running = true;
  let targetSpeed = prefersReduced ? 0 : baseSpeedPxPerSec;
  const speedState = { x: targetSpeed, v: 0 }; // x=speed, v=speed derivative
  let x = 0; // 初始位置：0 表示从右侧开始（translate3d 用正值）
  let lastT = performance.now();
  let lastAppliedX = NaN;

  function measureHalfWidth() {
    // track.scrollWidth 是两份内容的总宽度，half 即一份宽度
    // 使用 Math.floor 确保精度，避免浮点数误差
    return Math.floor(track.scrollWidth / 2);
  }

  function measureContainerWidth() {
    // 获取容器（marquee）的宽度，现在容器宽度为浏览器窗口宽度
    // 使用 Math.ceil 确保向上取整，避免精度问题
    return Math.ceil(root.getBoundingClientRect().width);
  }

  let halfWidth = 0;
  let containerWidth = 0;

  // 初始化测量（等一帧，确保布局稳定）
  requestAnimationFrame(() => {
    halfWidth = measureHalfWidth();
    containerWidth = measureContainerWidth();
    // 从容器右侧边缘进入：初始位置设为 containerWidth，让第一份内容从右侧外开始
    // 由于内容有两份，当第一份离开左侧时，第二份会无缝衔接
    if (halfWidth > 0 && containerWidth > 0) {
      x = containerWidth;
      // 立即应用初始位置，确保从右侧外开始
      applyX(x);
    }
  });

  // 监听窗口大小变化，更新容器宽度
  const handleResize = () => {
    const oldHalfWidth = halfWidth;
    const oldContainerWidth = containerWidth;
    halfWidth = measureHalfWidth();
    containerWidth = measureContainerWidth();
    // 重新对齐，避免 resize 后跳动过大
    // 保持相对位置比例，确保无缝循环
    if (oldHalfWidth > 0 && halfWidth > 0 && oldContainerWidth > 0 && containerWidth > 0) {
      // 计算相对于容器宽度的偏移量
      const relativeOffset = oldContainerWidth - x;
      // 保持相对位置比例
      const newRelativeOffset = (relativeOffset / oldHalfWidth) * halfWidth;
      // 转换为新的x值
      x = containerWidth - newRelativeOffset;
      // 确保在有效范围内
      if (x < containerWidth - halfWidth) {
        x = containerWidth - (newRelativeOffset % halfWidth);
      }
      if (x > containerWidth) {
        x = containerWidth - (newRelativeOffset % halfWidth);
      }
    }
  };
  window.addEventListener("resize", handleResize, { passive: true });

  // 拖拽/触摸：手动控制 x，并注入一个短暂的“手势速度”，随后回归自动速度
  let isDragging = false;
  let pointerId = null;
  let lastPointerX = 0;
  let lastPointerT = 0;
  let gestureSpeed = 0; // px/s，正数表示向右拖（内容向右移动）

  function applyX(newX) {
    // 无缝循环逻辑（确保真正无缝，无跳跃）：
    // 内容有两份，每份宽度为 halfWidth
    // 关键：让x从containerWidth开始减少，通过模运算实现无缝循环
    // 当第一份内容完全离开左侧时，第二份内容会无缝衔接
    if (halfWidth > 0 && containerWidth > 0) {
      // 将x转换为相对于halfWidth的偏移量
      // 当x从containerWidth减少到containerWidth - halfWidth时，第一份内容完全离开左侧
      // 此时重置x为containerWidth，第二份内容无缝衔接
      let relativeX = containerWidth - newX;
      
      // 处理超出范围的情况
      while (relativeX >= halfWidth) {
        relativeX = relativeX - halfWidth;
      }
      while (relativeX < 0) {
        relativeX = relativeX + halfWidth;
      }
      
      // 转换回x值
      newX = containerWidth - relativeX;
    }
    
    // 避免极小变化导致的合成抖动：小于 0.01px 不更新
    // 从容器右侧边缘进入：translate3d 用 -x
    // x = containerWidth 时，第一份内容的第一张卡片刚好在容器右侧外
    // x = containerWidth - halfWidth 时，第一份内容的最后一张卡片刚好离开容器左侧
    // 当 x 重置为 containerWidth 时，第二份内容会无缝衔接（因为内容有两份且完全相同）
    
    // 直接使用x作为offset，因为x本身就是从containerWidth开始的
    const offset = newX;
    
    // 检测重置：如果x从接近containerWidth - halfWidth突然变成接近containerWidth，说明重置了
    // 但由于内容有两份，当x重置时，第二份内容应该刚好无缝衔接
    // 所以不需要特殊处理，直接应用新的offset即可
    if (!Number.isFinite(lastAppliedX) || Math.abs(newX - lastAppliedX) > 0.01) {
      track.style.transform = `translate3d(${-offset}px, 0, 0)`;
      lastAppliedX = newX;
    }
    x = newX;
  }

  function tick(now) {
    if (!running) return;
    const dt = clamp((now - lastT) / 1000, 0, 0.05);
    lastT = now;

    // 实时更新容器宽度（应对窗口大小变化）
    containerWidth = measureContainerWidth();

    // 手势速度会指数衰减回 0（让拖拽放开后自然回归自动滚动）
    const gestureAlpha = expSmoothingAlpha(dt, 10.5);
    gestureSpeed += (0 - gestureSpeed) * gestureAlpha;

    // 用二阶弹簧让速度贴近目标：比单纯 lerp 更自然
    springStep(speedState, targetSpeed, dt, speedSpringHz, speedDamping);
    const autoSpeed = speedState.x;

    if (!prefersReduced) {
      if (!isDragging) {
        // 从浏览器窗口最右边边缘进入：x 减少时内容向左移动（视觉上从右侧进入、左侧离开），所以 autoSpeed 正数，x 减少
        // 让x持续减少（从容器宽度开始），通过applyX中的模运算实现无缝循环
        x -= (autoSpeed - gestureSpeed) * dt;
        applyX(x);
      }
    }

    requestAnimationFrame(tick);
  }

  requestAnimationFrame(tick);

  // hover：减速到停，离开恢复
  const onEnter = () => {
    targetSpeed = 0;
    // 通过“预置速度导数”让停下更像渐进刹车
    speedState.v *= 0.25;
  };
  const onLeave = () => {
    targetSpeed = prefersReduced ? 0 : baseSpeedPxPerSec;
    speedState.v *= 0.25;
  };

  root.addEventListener("mouseenter", onEnter, { passive: true });
  root.addEventListener("mouseleave", onLeave, { passive: true });

  // 交互：拖拽/触摸拖动（不抢滚动条，水平拖动为主）
  root.addEventListener("pointerdown", (e) => {
    if (prefersReduced) return;
    if (e.button !== undefined && e.button !== 0) return;
    isDragging = true;
    pointerId = e.pointerId;
    root.setPointerCapture(pointerId);
    root.classList.add("is-dragging");
    lastPointerX = e.clientX;
    lastPointerT = performance.now();
    gestureSpeed = 0;
    // 拖动时把自动目标速度降一点，避免“抢回去”的感觉
    targetSpeed = 0;
  });

  root.addEventListener("pointermove", (e) => {
    if (!isDragging || e.pointerId !== pointerId) return;
    const now = performance.now();
    const dx = e.clientX - lastPointerX;
    const dt = clamp((now - lastPointerT) / 1000, 0.001, 0.05);
    lastPointerX = e.clientX;
    lastPointerT = now;

    // 从右侧进入：x 减少时内容向左移动；手向右拖应让内容向右（x 增加），所以 x += dx
    applyX(x + dx);

    // 估计手势速度（px/s），用于放开后的惯性
    const inst = dx / dt; // px/s，右为正
    // 低通一下，减少手抖
    gestureSpeed = gestureSpeed * 0.6 + inst * 0.4;
  });

  function endDrag() {
    if (!isDragging) return;
    isDragging = false;
    root.classList.remove("is-dragging");
    try {
      if (pointerId != null) root.releasePointerCapture(pointerId);
    } catch {}
    pointerId = null;
    // 放开后恢复自动目标速度，并把“手势速度”带入（会在 tick 里衰减）
    targetSpeed = prefersReduced ? 0 : baseSpeedPxPerSec;
    speedState.v *= 0.35;
  }

  root.addEventListener("pointerup", endDrag);
  root.addEventListener("pointercancel", endDrag);
  root.addEventListener("lostpointercapture", endDrag);

  // 页面不可见时暂停（省电/更稳）
  const onVis = () => {
    if (document.hidden) {
      running = false;
    } else {
      running = true;
      lastT = performance.now();
      requestAnimationFrame(tick);
    }
  };
  document.addEventListener("visibilitychange", onVis, { passive: true });

  // 失焦时也停一下，回到页面再恢复（体验更像“丝滑播放器”）
  const onBlur = () => {
    targetSpeed = 0;
  };
  const onFocus = () => {
    if (!isDragging) targetSpeed = prefersReduced ? 0 : baseSpeedPxPerSec;
  };
  window.addEventListener("blur", onBlur, { passive: true });
  window.addEventListener("focus", onFocus, { passive: true });

  return () => {
    document.removeEventListener("visibilitychange", onVis);
    window.removeEventListener("blur", onBlur);
    window.removeEventListener("focus", onFocus);
    window.removeEventListener("resize", handleResize);
    root.removeEventListener("mouseenter", onEnter);
    root.removeEventListener("mouseleave", onLeave);
    running = false;
  };
}

// 背景视频处理：确保视频正确加载和循环播放
function setupBackgroundVideo() {
  const video = document.querySelector(".bg-video");
  if (!video) return;

  // 确保视频循环播放
  video.addEventListener("loadeddata", () => {
    video.play().catch((err) => {
      console.warn("视频自动播放失败:", err);
    });
  });

  // 视频结束时重新播放（确保无缝循环）
  video.addEventListener("ended", () => {
    video.currentTime = 0;
    video.play().catch((err) => {
      console.warn("视频循环播放失败:", err);
    });
  });

  // 处理视频加载错误
  video.addEventListener("error", () => {
    console.warn("背景视频加载失败，将使用备用背景");
    // 可以在这里添加备用背景图片
  });

  // 确保视频在页面可见时播放
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) {
      video.play().catch((err) => {
        console.warn("视频恢复播放失败:", err);
      });
    }
  });
}

document.addEventListener(
  "DOMContentLoaded",
  () => {
    // 设置背景视频
    setupBackgroundVideo();
    // 设置流动播放
    document.querySelectorAll("[data-marquee]").forEach((el) => setupMarquee(el));
  },
  { passive: true }
);


