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
            document.getElementById("L_Sim1").innerHTML = response['avg_clients_in_system'];
            document.getElementById("Lq_Sim1").innerHTML = response['avg_clients_in_line'];
            document.getElementById("W_Sim1").innerHTML = response['avg_system_time'];
            document.getElementById("Wq_Sim1").innerHTML = response['avg_waiting_time'];
            document.getElementById("E_Sim1").innerHTML = response['avg_waiting_time'];
            document.getElementById("S_Sim1").innerHTML = response['avg_number_of_departure'];
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
            document.getElementById("L_Sim2").innerHTML = response['avg_clients_in_system'];
            document.getElementById("Lq_Sim2").innerHTML = response['avg_clients_in_line'];
            document.getElementById("W_Sim2").innerHTML = response['avg_system_time'];
            document.getElementById("Wq_Sim2").innerHTML = response['avg_waiting_time'];
            document.getElementById("E_Sim2").innerHTML = response['avg_waiting_time'];
            document.getElementById("S_Sim2").innerHTML = response['avg_number_of_departure'];
            $('#loading2').html('Rodar simulação 2');
        },
        error: function (xhr) {
            alert("Ocorreu um erro: " + xhr.status + " " + xhr.statusText);
            $('#loading2').html('Rodar simulação 2');
        }
    });
}