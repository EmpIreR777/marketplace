// useScrollDrag.ts
import { onMounted, ref } from "vue";

export function useScrollDrag() {
  const scrollContainer = ref<HTMLElement | null>(null);

  onMounted(() => {
    const container = scrollContainer.value;

    if (!container) {
      console.error("Container reference is null.");
      return;
    }

    // For mouse events
    let isMouseDown = false;
    let startX = 0;
    let scrollLeft = 0;

    container.addEventListener("mousedown", (e) => {
      isMouseDown = true;
      startX = e.clientX;
      scrollLeft = container.scrollLeft;
      container.style.cursor = "grabbing";
    });

    container.addEventListener("mouseup", () => {
      isMouseDown = false;
      container.style.cursor = "grab";
    });

    container.addEventListener("mouseleave", () => {
      isMouseDown = false;
      container.style.cursor = "grab";
    });

    container.addEventListener("mousemove", (e) => {
      if (!isMouseDown) return;
      e.preventDefault();
      const x = e.clientX;
      const walk = (x - startX) * 2; // Scroll speed
      container.scrollLeft = scrollLeft - walk;
    });

    // For touch events
    let startTouchX = 0;
    let startTouchScrollLeft = 0;

    container.addEventListener("touchstart", (e) => {
      const touch = e.touches[0];
      startTouchX = touch.clientX;
      startTouchScrollLeft = container.scrollLeft;
    });

    container.addEventListener("touchmove", (e) => {
      const touch = e.touches[0];
      const x = touch.clientX;
      const walk = (x - startTouchX) * 2; // Scroll speed
      container.scrollLeft = startTouchScrollLeft - walk;
    });
  });

  return {
    scrollContainer,
  };
}
