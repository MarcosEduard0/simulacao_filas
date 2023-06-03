function analitico() {
    var lamb = parseFloat(document.getElementById("arrivalRate").value);
    var mi = parseFloat(document.getElementById("serviceRate").value);
    var c = parseFloat(document.getElementById("initial_customers").value);
    var deterministic = document.getElementById("SelectDeterministicMi").value;
    var ro, lq, wq, w, l, b, bc, uc;
    if (deterministic === "0") {
        ro = lamb / mi;
        lq = ro * ro / (1 - ro);
        wq = ro / (mi - lamb);
        w = 1 / (mi - lamb);
        l = ro / (1 - ro);
        b = c ? 1/(mi-lamb) : 0
        bc = c/(mi-lamb)
        uc = c < 2 ? 0 : c-1
    } else {
        ro = lamb / mi;
        lq = (ro**2) / (2 * (1 - ro));
        wq = lq / lamb;
        w = wq + (1 / mi);
        l = lamb * w;
        b = 0
        bc = 0
        uc = 0
    }
    document.getElementById("L_Ana").innerHTML = l.toFixed(2);
    document.getElementById("Lq_Ana").innerHTML = lq.toFixed(2);
    document.getElementById("W_Ana").innerHTML = w.toFixed(2);
    document.getElementById("Wq_Ana").innerHTML = wq.toFixed(2);
    document.getElementById("B_Ana").innerHTML = b.toFixed(2);
    document.getElementById("Bc_Ana").innerHTML = bc.toFixed(2);
    document.getElementById("Uc_Ana").innerHTML = uc.toFixed(2);
}


function chamarSimulacao1() {
    $('#loading1').html('<span class="spinner-border spinner-border-sm" role="status" role="status" aria-hidden="true"></span> Simulando...');
    lamb = document.getElementById("arrivalRate").value
    mi = document.getElementById("serviceRate").value
    total_time = document.getElementById("expduration").value
    sample_size = document.getElementById("sample_size").value
    initial_customers = document.getElementById("initial_customers").value
    deterministic = document.getElementById("SelectDeterministicMi").value
    $.ajax({
        url: "/simulador1",
        method: "POST",
        data: { lamb: lamb, mi: mi, total_time: total_time, sample_size:sample_size, deterministic: deterministic, initial_customers:initial_customers },
        success: function (response) {
            document.getElementById("L_Sim1").innerHTML = response['L'];
            document.getElementById("Lq_Sim1").innerHTML = response['Lq'];
            document.getElementById("W_Sim1").innerHTML = response['W'];
            document.getElementById("Wq_Sim1").innerHTML = response['Wq'];
            document.getElementById("E_Sim1").innerHTML = response['Wq'];
            document.getElementById("S_Sim1").innerHTML = response['S'];
            document.getElementById("B_Sim1").innerHTML = response['B'];
            document.getElementById("Bc_Sim1").innerHTML = response['Bc'];
            document.getElementById("Uc_Sim1").innerHTML = initial_customers < 2 ? 0 : response['Uc']; 

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
    initial_customers = document.getElementById("initial_customers").value
    deterministic = document.getElementById("SelectDeterministicMi").value
    $.ajax({
        url: "/simulador2",
        method: "POST",
        data: { lamb: lamb, mi: mi, total_time: total_time, sample_size:sample_size, deterministic: deterministic, initial_customers:initial_customers  },
        success: function (response) {
            document.getElementById("L_Sim2").innerHTML = response['L'];
            document.getElementById("Lq_Sim2").innerHTML = response['Lq'];
            document.getElementById("W_Sim2").innerHTML = response['W'];
            document.getElementById("Wq_Sim2").innerHTML = response['Wq'];
            document.getElementById("E_Sim2").innerHTML = response['Wq'];
            document.getElementById("S_Sim2").innerHTML = response['S'];
            document.getElementById("B_Sim2").innerHTML = response['B'];
            document.getElementById("Bc_Sim2").innerHTML = response['Bc'];
            document.getElementById("Uc_Sim2").innerHTML = initial_customers < 2 ? 0 : response['Uc']; 
            $('#loading2').html('Rodar simulação 2');
        },
        error: function (xhr) {
            alert("Ocorreu um erro: " + xhr.status + " " + xhr.statusText);
            $('#loading2').html('Rodar simulação 2');
        }
    });
}