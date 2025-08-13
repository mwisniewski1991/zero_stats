// Main JavaScript file for YouTube Statistics Dashboard

// Utility functions
function formatNumber(num) {
    return new Intl.NumberFormat('pl-PL').format(num);
}

function formatDate(dateString) {
    if (!dateString) return 'Brak daty';
    const date = new Date(dateString);
    return date.toLocaleDateString('pl-PL');
}

// Add loading state to buttons
function addLoadingState(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<span class="loading"></span> Ładowanie...';
    button.disabled = true;
    return originalText;
}

function removeLoadingState(button, originalText) {
    button.innerHTML = originalText;
    button.disabled = false;
}

// Smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling to all anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add active state to navigation
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Add tooltips to elements with data-bs-toggle="tooltip"
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add copy to clipboard functionality
    const copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-clipboard-text');
            if (textToCopy) {
                navigator.clipboard.writeText(textToCopy).then(function() {
                    // Show success message
                    const originalText = button.innerHTML;
                    button.innerHTML = 'Skopiowano!';
                    button.classList.add('btn-success');
                    button.classList.remove('btn-outline-secondary');
                    
                    setTimeout(() => {
                        button.innerHTML = originalText;
                        button.classList.remove('btn-success');
                        button.classList.add('btn-outline-secondary');
                    }, 2000);
                });
            }
        });
    });
});

// Chart utility functions
function createBarChart(containerId, data, options = {}) {
    const defaults = {
        width: 600,
        height: 400,
        margin: {top: 20, right: 30, bottom: 90, left: 60},
        xField: 'name',
        yField: 'value',
        color: '#69b3a2',
        title: 'Chart'
    };
    
    const config = { ...defaults, ...options };
    
    // Clear container
    d3.select(`#${containerId}`).html('');
    
    const svg = d3.select(`#${containerId}`)
        .append("svg")
        .attr("width", config.width + config.margin.right + config.margin.left)
        .attr("height", config.height + config.margin.top + config.margin.bottom)
        .append("g")
        .attr("transform", `translate(${config.margin.left},${config.margin.top})`);
    
    // X axis
    const x = d3.scaleBand()
        .range([0, config.width])
        .domain(data.map(d => d[config.xField]))
        .padding(0.2);
    
    svg.append("g")
        .attr("transform", `translate(0,${config.height})`)
        .call(d3.axisBottom(x))
        .selectAll("text")
        .attr("transform", "translate(-10,0)rotate(-45)")
        .style("text-anchor", "end");
    
    // Y axis
    const y = d3.scaleLinear()
        .domain([0, d3.max(data, d => d[config.yField])])
        .range([config.height, 0]);
    
    svg.append("g")
        .call(d3.axisLeft(y).tickFormat(d3.format(",")));
    
    // Bars
    svg.selectAll("mybar")
        .data(data)
        .join("rect")
        .attr("x", d => x(d[config.xField]))
        .attr("y", d => y(d[config.yField]))
        .attr("width", x.bandwidth())
        .attr("height", d => config.height - y(d[config.yField]))
        .attr("fill", config.color)
        .on("mouseover", function(event, d) {
            d3.select(this).attr("fill", d3.color(config.color).darker(0.3));
            
            // Tooltip
            svg.append("text")
                .attr("class", "tooltip")
                .attr("x", x(d[config.xField]) + x.bandwidth() / 2)
                .attr("y", y(d[config.yField]) - 10)
                .attr("text-anchor", "middle")
                .text(formatNumber(d[config.yField]));
        })
        .on("mouseout", function(event, d) {
            d3.select(this).attr("fill", config.color);
            svg.selectAll(".tooltip").remove();
        });
    
    // Add title
    svg.append("text")
        .attr("x", config.width / 2)
        .attr("y", -5)
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("font-weight", "bold")
        .text(config.title);
}

// Error handling
function showError(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Success message
function showSuccess(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-success alert-dismissible fade show';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-dismiss after 3 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 3000);
} 