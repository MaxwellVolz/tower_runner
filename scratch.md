
lets set up a def check_for_tower that will

- use the return of capture_area (aka return cv2.cvtColor(capture_np, cv2.COLOR_BGR2RGB))
- and search for a color close to RGB 170, 70, 180
example for using contours:

```py
    lower = np.array([5, 170, 230])
    upper = np.array([30, 200, 255])
    mask = cv2.inRange(screen_np, lower, upper)
    kernel = np.ones((5, 5), np.uint8)

    mask_processed = cv2.dilate(mask, kernel, iterations=1)
    mask_processed = cv2.erode(mask_processed, kernel, iterations=1)

    contours, _ = cv2.findContours(
        mask_processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )


    if not contours:
        print("No areas to monitor.")
        return False  # Signal to exit monitoring

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        watch_x = x - 18  # Position the watch area
        watch_y = y + (h // 2) - 3
        watch_areas.append((watch_x, watch_y, 7, 7))  # Store area

        cv2.rectangle(screen_np, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.rectangle(
            screen_np,
            (watch_x, watch_y),
            (watch_x + 6, watch_y + 6),
            (255, 255, 0),
            2,
        )

        
    cv2.imwrite(
        "screen_with_rectangles.png", cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)
    )
```
        

 find_the_tower that will