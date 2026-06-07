// ==========================
// REVENUE BY REGION
// ==========================

const regionCtx = document
    .getElementById("regionChart")
    .getContext("2d");

new Chart(regionCtx, {

    type: "bar",

    data: {
        labels: regionLabels,

        datasets: [{
            label: "Revenue",

            data: regionValues,

            borderWidth: 2,

            borderRadius: 8,

            backgroundColor: [
                "#38bdf8",
                "#22c55e",
                "#f97316",
                "#a855f7"
            ]
        }]
    },

    options: {

        responsive: true,

        plugins: {

            legend: {
                labels: {
                    color: "#ffffff"
                }
            }
        },

        scales: {

            x: {
                ticks: {
                    color: "#ffffff"
                },

                grid: {
                    color: "rgba(255,255,255,0.05)"
                }
            },

            y: {
                ticks: {
                    color: "#ffffff"
                },

                grid: {
                    color: "rgba(255,255,255,0.05)"
                }
            }
        }
    }
});


// ==========================
// PRODUCT REVENUE
// ==========================

const productCtx = document
    .getElementById("productChart")
    .getContext("2d");

new Chart(productCtx, {

    type: "doughnut",

    data: {

        labels: productLabels,

        datasets: [{

            data: productValues,

            backgroundColor: [
                "#38bdf8",
                "#22c55e",
                "#f97316",
                "#a855f7",
                "#ef4444",
                "#14b8a6",
                "#eab308",
                "#6366f1"
            ]
        }]
    },

    options: {

        responsive: true,

        plugins: {

            legend: {

                position: "bottom",

                labels: {
                    color: "#ffffff"
                }
            }
        }
    }
});


// ==========================
// MONTHLY TREND
// ==========================

const monthlyCtx = document
    .getElementById("monthlyChart")
    .getContext("2d");

new Chart(monthlyCtx, {

    type: "line",

    data: {

        labels: monthLabels,

        datasets: [{

            label: "Monthly Revenue",

            data: monthValues,

            fill: true,

            tension: 0.4,

            borderWidth: 3,

            borderColor: "#38bdf8",

            backgroundColor:
            "rgba(56,189,248,0.15)",

            pointRadius: 5,

            pointBackgroundColor:
            "#38bdf8"
        }]
    },

    options: {

        responsive: true,

        plugins: {

            legend: {

                labels: {
                    color: "#ffffff"
                }
            }
        },

        scales: {

            x: {

                ticks: {
                    color: "#ffffff"
                },

                grid: {
                    color: "rgba(255,255,255,0.05)"
                }
            },

            y: {

                ticks: {
                    color: "#ffffff"
                },

                grid: {
                    color: "rgba(255,255,255,0.05)"
                }
            }
        }
    }
});


// ==========================
// CARD ANIMATION
// ==========================

const cards = document.querySelectorAll(".card");

cards.forEach((card, index) => {

    card.style.opacity = "0";
    card.style.transform = "translateY(30px)";

    setTimeout(() => {

        card.style.transition =
            "all 0.6s ease";

        card.style.opacity = "1";
        card.style.transform =
            "translateY(0)";

    }, index * 150);

});


// ==========================
// ML CARD ANIMATION
// ==========================

const mlCards =
    document.querySelectorAll(".ml-card");

mlCards.forEach((card, index) => {

    card.style.opacity = "0";

    setTimeout(() => {

        card.style.transition =
            "all 0.5s ease";

        card.style.opacity = "1";

    }, index * 250);

});