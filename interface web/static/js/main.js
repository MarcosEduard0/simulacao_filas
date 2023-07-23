function analitico() {
    var lamb = parseFloat(document.getElementById("arrivalRate").value);
    var mi = parseFloat(document.getElementById("serviceRate").value);
    var deterministic = document.getElementById("SelectDeterministicMi").value;

    var ro, lq, wq, w, l;
    if (deterministic === "0") {
        ro = lamb / mi;
        lq = ro * ro / (1 - ro);
        wq = ro / (mi - lamb);
        w = 1 / (mi - lamb);
        l = ro / (1 - ro);
    } else {
        ro = lamb / mi;
        lq = (ro**2) / (2 * (1 - ro));
        wq = lq / lamb;
        w = wq + (1 / mi);
        l = lamb * w;
    }
    document.getElementById("L_Ana").innerHTML = l.toFixed(2);
    document.getElementById("Lq_Ana").innerHTML = lq.toFixed(2);
    document.getElementById("W_Ana").innerHTML = w.toFixed(2);
    document.getElementById("Wq_Ana").innerHTML = wq.toFixed(2);
    document.getElementById("p0_Ana").innerHTML = ro.toFixed(2);
    document.getElementById("p_Ana").innerHTML = (1-ro).toFixed(2);
}


function chamarSimulacao1() {
    $('#loading1').html('<span class="spinner-border spinner-border-sm" role="status" role="status" aria-hidden="true"></span> Simulando...');
    lamb = document.getElementById("arrivalRate").value
    mi = document.getElementById("serviceRate").value
    total_time = document.getElementById("expduration").value
    sample_size = document.getElementById("sample_size").value
    deterministic = document.getElementById("SelectDeterministicMi").value
    $.ajax({
        url: "/simulador1",
        method: "POST",
        data: { lamb: lamb, mi: mi, total_time: total_time, sample_size:sample_size, deterministic: deterministic },
        success: function (response) {
            document.getElementById("L_Sim1").innerHTML = response['L'];
            document.getElementById("Lq_Sim1").innerHTML = response['Lq'];
            document.getElementById("W_Sim1").innerHTML = response['W'];
            document.getElementById("Wq_Sim1").innerHTML = response['Wq'];
            document.getElementById("p0_Sim1").innerHTML = response['rho'];
            document.getElementById("p_Sim1").innerHTML = (1-response['rho']).toFixed(2);
            $('#loading1').html('Rodar simulação 1');
        },
        error: function (xhr) {
            alert("Ocorreu um erro: " + xhr.status + " " + xhr.statusText);
            $('#loading1').html('Rodar simulação 1');
        }
    });
}

function chamarSimulacao2() {
    $('#loading2').html('<span class="spinner-border spinner-border-sm" role="status" role="status" aria-hidden="true"></span> Simulando...');
    lamb = document.getElementById("arrivalRate").value
    mi = document.getElementById("serviceRate").value
    total_time = document.getElementById("expduration").value
    sample_size = document.getElementById("sample_size").value
    deterministic = document.getElementById("SelectDeterministicMi").value
    $.ajax({
        url: "/simulador2",
        method: "POST",
        data: { lamb: lamb, mi: mi, total_time: total_time, sample_size:sample_size, deterministic: deterministic },
        success: function (response) {
            document.getElementById("L_Sim2").innerHTML = response['L'];
            document.getElementById("Lq_Sim2").innerHTML = response['Lq'];
            document.getElementById("W_Sim2").innerHTML = response['W'];
            document.getElementById("Wq_Sim2").innerHTML = response['Wq'];
            document.getElementById("p0_Sim2").innerHTML = response['rho'];
            document.getElementById("p_Sim2").innerHTML = (1-response['rho']).toFixed(2);
            $('#loading2').html('Rodar simulação 2');
        },
        error: function (xhr) {
            alert("Ocorreu um erro: " + xhr.status + " " + xhr.statusText);
            $('#loading2').html('Rodar simulação 2');
        }
    });
}