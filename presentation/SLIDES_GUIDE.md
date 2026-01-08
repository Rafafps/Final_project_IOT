# 📊 Guide for Creating Presentation Slides

## 📝 Base File Created

The file **`PRESENTATION_SLIDES.md`** (in this directory) has been created with the complete slide content in Markdown format.

## 🎯 Options to Convert to Slides

### Option 1: Marp (Recommended - Easiest)

**Marp** converts Markdown directly to PowerPoint/PDF.

1. **Install Marp CLI:**
   ```bash
   npm install -g @marp-team/marp-cli
   ```

2. **Convert to PDF:**
   ```bash
   marp PRESENTATION_SLIDES.md --pdf
   ```

3. **Convert to PowerPoint:**
   ```bash
   marp PRESENTATION_SLIDES.md --pptx
   ```

**Or use the online editor:** https://marp.app/

---

### Option 2: PowerPoint/Google Slides (Manual)

1. Open PowerPoint or Google Slides
2. Copy content from each slide in `PRESENTATION_SLIDES.md`
3. Create slides following the structure:
   - Slide 1: Title
   - Slide 2: Scenario
   - Slide 3: Devices
   - Slide 4: Architecture (use component diagram)
   - Slide 5: Closed Loop (use sequence diagram)
   - Slide 6: Protocols
   - Slide 7: Data
   - Slide 8: Rules
   - Slide 9: Demo
   - Slide 10: Conclusions
   - Slide 11: Questions

---

### Option 3: Reveal.js (HTML)

1. Use a Reveal.js template
2. Copy Markdown content
3. Generate interactive HTML

---

## 🎨 Visual Elements to Include

### Diagrams (Export as PNG)

1. **Component Diagram:**
   - Access: https://mermaid.live
   - Paste component diagram code
   - Export as PNG
   - Add to Slide 4

2. **Sequence Diagram (Closed Loop):**
   - Access: https://mermaid.live
   - Paste sequence diagram code
   - Export as PNG
   - Add to Slide 5

3. **Deployment Diagram:**
   - Optional but recommended
   - Add to Slide 4 or 6

---

### Screenshots for Demo (Slide 9)

1. **Swagger UI:**
   - `http://localhost:7070/docs`
   - Screenshot of interface

2. **Telemetry:**
   - Screenshot of `/telemetry` endpoint
   - Showing received data

3. **Alerts:**
   - Screenshot of `/alerts` endpoint
   - Showing generated alerts

4. **Terminal:**
   - Screenshot of running devices
   - Showing publication logs

---

## ✅ Slides Checklist

- [ ] Slide 1: Title and participants
- [ ] Slide 2: Application scenario
- [ ] Slide 3: IoT Devices (4 devices)
- [ ] Slide 4: Architecture (component diagram)
- [ ] Slide 5: **Closed Loop** (sequence diagram) - **ESSENTIAL**
- [ ] Slide 6: Protocols and technologies
- [ ] Slide 7: Data structure (JSON)
- [ ] Slide 8: Business rules
- [ ] Slide 9: **Demo** (screenshots or video)
- [ ] Slide 10: Conclusions
- [ ] Slide 11: Questions

---

## 🎤 Presentation Tips

### Time: 10-15 minutes

1. **Introduction (2 min):**
   - Present the scenario
   - Explain the problem

2. **Architecture (3 min):**
   - Show components
   - Explain data flow

3. **Closed Loop (2 min):** ⭐ **HIGHLIGHT THIS**
   - Explain how it works
   - Show sequence diagram
   - **It's mandatory to show it works!**

4. **Demo (3 min):** ⭐ **ESSENTIAL**
   - Run system live
   - Show telemetry arriving
   - Trigger a rule (water >= 350)
   - Show command being sent
   - **Have screenshots as backup!**

5. **Conclusions (1 min):**
   - Summarize what was done
   - Mention learnings

---

## 🚨 Demo Preparation

### Before Presentation:

1. **Test everything:**
   ```bash
   # Start broker
   mosquitto -p 1883 -v
   
   # Start manager
   uvicorn manager.api_server:app --host 0.0.0.0 --port 7070
   
   # Run devices
   python3 devices/water_sensor.py
   ```

2. **Prepare screenshots:**
   - Swagger UI open
   - Telemetry being received
   - Generated alerts
   - Terminal with logs

3. **Prepare test values:**
   - Force water_sensor to publish >= 350 cm
   - Or temporarily modify threshold

4. **Have backup:**
   - Recorded demo video
   - Screenshots of each step
   - Commented code ready to show

---

## 📚 Useful Resources

- **Mermaid Live:** https://mermaid.live (for diagrams)
- **Marp:** https://marp.app (to convert Markdown)
- **Draw.IO:** https://app.diagrams.net (alternative for diagrams)
- **Screenshot Tool:** `gnome-screenshot` or `flameshot`

---

## 💡 Final Tip

**The most important thing is to show the closed loop working!** If the live demo fails, use screenshots and explain what would happen. The teacher wants to see that you understand the concept and implemented it correctly.

Good luck! 🚀
