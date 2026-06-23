// /** @odoo-module **/
import { registry } from "@web/core/registry";
import { loadJS } from "@web/core/assets";

const CHARTJS = "/web/static/lib/Chart/Chart.js";
async function ensureChartJsLoaded(){
    if(window.Chart)
        return;
    await loadJS(CHARTJS);
}

function renderChart(canvas){
    if(canvas.dataset.chartRendered === "1")
        return;
    const raw = canvas.getAttribute("data-chart");
    if(!raw)
        return;
    let parsed;
    try{
        parsed = JSON.parse(raw);
    } catch(e){
        console.warn("[mitienda] No se pudo parsear data-chart",e);
        return;
    }
    const labels = parsed.labels || [];
    const data = parsed.data || [];
    
    new window.Chart(canvas, {
        type:"bar",
        data:{
            labels,
            datasets:[
                {
                    label:"Sincronizaciones",
                    data,
                    backgroundColor: "#7ab9b9",
                    borderRadius: 4,
                    maxBarThickness: 45,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins:{
                legend:{display: false },
                tooltip:{
                    enabled: true,
                    callback:{
                        label: function(context){
                            return ' ' + context.parsed.y + ' sincronizaciones';
                        } 
                    } 
                }  
            }, 
            scales: {
                y: {display: false,},
                x: {grid:{display: false,}, ticks:{maxTicksLimit: 7}} 
            },
            scales:{
                y:{
                    beginAtZero: true,
                    display: false,
                },
            },
        },
    });
    canvas.dataset.chartRendered = "1";
}

function scanAndRender(){
    const canvases = document.querySelectorAll(".o_mitienda_sync_chart");
    canvases.forEach(renderChart);
}

registry.category("services").add("mitienda_sync_chart_service",{
    async start(){
        await ensureChartJsLoaded();
        scanAndRender();
        const observer = new MutationObserver(()=>{
            scanAndRender();
        });
        observer.observe(document.body,{childList: true, subtree:true});
    },
});


registry.category("services").add("mitienda_pv_click_handler",{
    start(env){
        document.addEventListener("click", (ev) => {
            const link = ev.target.closest(".o_siat_pv_name");
            if(!link)
                return;
            ev.preventDefault();
            ev.stopPropagation();
            const saleId = link.dataset.saleId;
            const pvId = link.dataset.pvId;

            if(saleId){
                env.services.action.doAction({
                    type:"ir.actions.act_window",
                    res_model:"sale.order",
                    res_id:parseInt(saleId,10),
                    views:[[false,"form"]],
                    target:"current",
                });
            } else if (pvId){
                env.services.action.doAction({
                    type:"ir.actions.act_window",
                    res_model:"siat.punto.venta",
                    res_id: parseInt(pvId,10),
                    views:[[false,"form"]],
                    target:"current",
                });
            }
            
        });
  },
});
