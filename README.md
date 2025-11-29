# Smart Task Analyzer

A lightweight full-stack app that scores and prioritizes tasks based on how urgent, important, time-consuming, and interconnected they are. The goal is simple — help users figure out what to work on first without overthinking it.

---

## What This App Does

- Takes a list of tasks with fields like due date, importance, effort, and dependencies  
- Calculates a smart priority score for each task  
- Sorts tasks from most important → least  
- Lets the user pick different strategies (fastest task, most important, deadline heavy, or balanced)  
- Shows clean, color-coded results in the frontend  
- Offers a basic “Top 3 tasks to do today” suggestion API

---

## How the Scoring Works

The scoring blends four things:

### **1. Urgency**
How close the deadline is.  
Tasks due today or overdue rise to the top.  
Tasks due far away naturally drop lower.

### **2. Importance**
A simple 1–10 scale from the user.  
Higher = more impact, so they get bumped.

### **3. Effort**
Quick tasks are easier wins.  
A task that takes 1 hour gets a higher effort score than one that takes 10.

### **4. Dependencies**
If Task A blocks Task B and C, A becomes more valuable because doing it unlocks more work.

### Final Score
The final score is a weighted blend of all four factors.  
Weights change based on strategy:

- **Smart Balance**: evenly blends everything  
- **Fastest Wins**: favors low-effort tasks  
- **High Impact**: favors importance  
- **Deadline Driven**: heavily favors urgency  

This makes the system flexible and realistic — different days require different decision styles.
