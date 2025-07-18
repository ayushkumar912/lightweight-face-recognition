# 🔍 Complete Prometheus Navigation Guide

## 📊 **Main Prometheus Interface Sections**

### **1. 🎯 Graph Tab (Main Query Interface)**
**URL:** http://localhost:9090/graph

**What you can do:**
- Execute PromQL queries
- View metrics in table or graph format
- Set time ranges for historical data
- Export query results

### **2. 🎯 Targets Tab (Service Health)**
**URL:** http://localhost:9090/targets

**What you can see:**
- All monitored services status
- Scrape intervals and last scrape times
- Error messages for failed targets
- Endpoint health (UP/DOWN)

### **3. 🎯 Service Discovery Tab**
**URL:** http://localhost:9090/service-discovery

**What you can monitor:**
- Dynamic service discovery status
- Discovered target information
- Service metadata

### **4. 🎯 Configuration Tab**
**URL:** http://localhost:9090/config

**What you can view:**
- Current Prometheus configuration
- Scrape job definitions
- Alert rules configuration
- Global settings

### **5. 🎯 Rules Tab**
**URL:** http://localhost:9090/rules

**What you can check:**
- Recording rules status
- Alert rules and their states
- Rule evaluation times

### **6. 🎯 Alerts Tab** 
**URL:** http://localhost:9090/alerts

**What you can monitor:**
- Active alerts
- Alert history
- Alert severity levels

### **7. 🎯 Status Tabs**
**Command Line:** http://localhost:9090/status/command-line
**Configuration:** http://localhost:9090/status/config
**Runtime Info:** http://localhost:9090/status/runtimeinfo
**Build Info:** http://localhost:9090/status/buildinfo
**TSDB Status:** http://localhost:9090/status/tsdb

---

## 🔍 **Key PromQL Queries for Your System**

### **Service Health Monitoring:**
```promql
# Check which services are up
up

# Services that are down
up == 0

# Uptime percentage over last hour
avg_over_time(up[1h]) * 100
```

### **System Performance:**
```promql
# Prometheus internal metrics
prometheus_tsdb_head_samples_appended_total

# Rule evaluation duration
prometheus_rule_evaluation_duration_seconds

# Query duration
prometheus_engine_query_duration_seconds
```

### **Target Information:**
```promql
# Number of targets
prometheus_sd_discovered_targets

# Scrape duration
prometheus_target_scrape_duration_seconds

# Scrapes per second
rate(prometheus_tsdb_head_samples_appended_total[5m])
```

---

## 📊 **Step-by-Step: How to View Details**

### **Step 1: Open Prometheus**
- Go to: http://localhost:9090
- You'll see the main Graph interface

### **Step 2: Check Service Status**
- Click "Status" → "Targets"
- View all monitored services
- Check UP/DOWN status

### **Step 3: Run Basic Queries**
- In Graph tab, enter: `up`
- Click "Execute"
- Switch between "Table" and "Graph" view

### **Step 4: Explore Metrics**
- Use autocomplete in query box
- Type metric names to see suggestions
- Use time range picker for historical data

### **Step 5: View Configuration**
- Click "Status" → "Configuration"
- See current scrape jobs
- Check target endpoints

---

## 🎯 **Advanced Query Examples**

### **Memory Usage:**
```promql
# Prometheus memory usage
prometheus_tsdb_head_series

# Memory growth rate
rate(prometheus_tsdb_head_series[5m])
```

### **Query Performance:**
```promql
# Slow queries
prometheus_engine_query_duration_seconds > 0.1

# Query rate
rate(prometheus_engine_queries_total[5m])
```

### **Storage Metrics:**
```promql
# Storage size
prometheus_tsdb_size_bytes

# Disk usage growth
rate(prometheus_tsdb_size_bytes[1h])
```

---

## 🔧 **Quick Navigation Tips**

1. **Auto-complete:** Start typing metric names in query box
2. **Time ranges:** Use preset ranges (5m, 1h, 1d) or custom
3. **Table vs Graph:** Toggle views for different perspectives  
4. **Export:** Download query results as CSV
5. **Permalink:** Share specific queries via URL
6. **Keyboard shortcuts:** Ctrl+Enter to execute queries
