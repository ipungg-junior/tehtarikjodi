
var noHp = document.getElementById('input-nomor-hp');
var inBiayaInvest = document.getElementById('input-biaya-investasi');
var inputJumlahCup = document.getElementById('input-jumlah-cup');
var inputJumlahHari = document.getElementById('input-jumlah-hari');
var inputOmsetKotor = document.getElementById('input-omset-kotor');
var inputHpp = document.getElementById('input-hpp');
var inputLabaKotor = document.getElementById('input-laba-kotor');
var inputOperasional = document.getElementById('input-beban-operasional');
var inputLainLain = document.getElementById('input-lain-lain');
var inputKaryawan = document.getElementById('input-karyawan');
var inputListrik = document.getElementById('input-listrik');
var inputSewaBangunan = document.getElementById('input-sewa-bangunan');

var groupOmset = document.getElementById('group-omset');
var groupHpp = document.getElementById('group-hpp');
var groupLabaKotor = document.getElementById('group-laba-kotor');
var groupLabaBersih = document.getElementById('group-laba-bersih');
var groupOperasional = document.getElementById('group-operasional');
var groupBEP = document.getElementById('group-bep');
var outputlaba = document.getElementById('output-lababersih');
const btnBEP = document.getElementById('btn-bep');
const btnReset = document.getElementById('btn-reset');
const btnPreview = document.getElementById('btn-preview');
const btnKalkulasi = document.getElementById('btn-kalkulasi');
const btnSimpan = document.getElementById('btn-simpan');
var stateAutoCalculate = false;
var gajiKaryawan = 0;
var biayaListrik = 0;
var biayaLain = 0;
var hargaPcup = 10000;
var totalOperasional = 0;
var bep = 0;
var labaBersih = 0;
var labaKotor = 0;
var hpp = 0;
var idCookie;

function getCookie(name) {
    var cookieArray = document.cookie.split("; ");
    for (var i = 0; i < cookieArray.length; i++) {
        var cookie = cookieArray[i];
        var parts = cookie.split("=");
        var cookieName = parts[0];
        var cookieValue = parts[1];
        if (cookieName === name) {
            return cookieValue;
        }
    }
    return null; // Return null jika cookie tidak ditemukan
}

function cekTeks() {
    // Dapatkan nilai dari input teks

    // Buat ekspresi reguler untuk mencocokkan huruf
    var regex = /[A-Za-z]/;

    // Periksa apakah input mengandung huruf
    if (regex.test(noHp.value)) {
        alert("Nomor Telepon tidak valid!");
        return false;
    } else {
        if ((noHp.value).length > 13) {
            alert("Total karakter lebih dari 13!");
            return false;
        } else {
            return true;
        }
    }

}

var statNomor = cekTeks();


function formatRupiah(angka) {
    var numberString = angka.toString();
    var sisa = numberString.length % 3;
    var rupiah = numberString.substr(0, sisa);
    var ribuan = numberString.substr(sisa).match(/\d{3}/g);

    if (ribuan) {
        var separator = sisa ? '.' : '';
        rupiah += separator + ribuan.join('.');
    }

    return rupiah;
}
function hapusTitik(inputText) {
    // Periksa apakah inputText mengandung titik
    if (inputText.includes('.')) {
        // Jika ada titik, hapus titik
        return parseInt(inputText.replace(/\./g, ''), 10);
    } else {
        // Jika tidak ada titik, kembalikan nilai asli
        return parseInt(inputText);
    }
}

// Bussiness Logic Function
inputJumlahHari.addEventListener('change', function () {
    // countdown auto calculate laba bersih jika hari sudah di input akan aktif
    stateAutoCalculate = true;
    groupOmset.classList.remove('hide');
    groupHpp.classList.remove('hide');
    groupLabaKotor.classList.remove('hide');
    var omsetKotor = 0;
    var lbkotor = 0;
    // omset kotor = jumlahcup X harga per cup X jumlahhari
    omsetKotor = (inputJumlahCup.options[inputJumlahCup.selectedIndex].value) * (hargaPcup) * (inputJumlahHari.options[inputJumlahHari.selectedIndex].value);
    hpp = (omsetKotor * 50) / 100;
    lbkotor = omsetKotor - hpp;
    inputOmsetKotor.value = formatRupiah(omsetKotor);
    inputHpp.value = formatRupiah(hpp);
    inputLabaKotor.value = formatRupiah(lbkotor);
    labaKotor = lbkotor;
})

btnKalkulasi.addEventListener('click', function () {
    var sewabangunan = hapusTitik(inputSewaBangunan.value);
    inputSewaBangunan.value = formatRupiah(sewabangunan);
    labaBersih = labaKotor - (totalOperasional)
    outputlaba.textContent = formatRupiah(labaBersih);
    // Hitung BEP
    bep = Math.round((14500000 + sewabangunan) / labaBersih);
    groupLabaBersih.classList.remove('hide');
    groupBEP.classList.remove('hide');
    btnBEP.textContent = bep + " Bulan";
    btnPreview.style.display = 'initial';
    stateAutoCalculate = false;

})


btnPreview.addEventListener('click', function () {
    var dataToSend = {
        no_hp: noHp.value,
        jumlah_cup: (inputJumlahCup.options[inputJumlahCup.selectedIndex].value),
        omset_kotor: inputOmsetKotor.value,
        hpp: formatRupiah(hpp),
        laba_kotor: formatRupiah(labaKotor),
        karyawan: formatRupiah(hapusTitik(inputKaryawan.value)),
        listrik: inputListrik.value,
        biaya_lain: inputLainLain.value,
        sewa_bangunan: inputSewaBangunan.value,
        bep: bep,
        laba_bersih: formatRupiah(labaBersih),
        operasional: totalOperasional
    }
    if (statNomor) {
        var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        //push data to server
        fetch('/simulasi-investasi/post-calculate/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dataToSend)
        }).then(function (response) {
            if (!response.ok) {
                alert('Gagal mengirim data, coba lagi.');
            }
            return response.json(); // Mengembalikan respons sebagai JSON
        }).then(function (data) {
            // Mengambil nilai dari kunci 'status_login'
            var statusLogin = data['status'];
            // Menampilkan nilai 'status_login' dalam konsol
            console.log(statusLogin);
            if (statusLogin == '200') {
                window.location = '/simulasi-investasi/report/';
            } else {
                window.location = '/simulasi-investasi/';
            }

            // Tempatkan kode selanjutnya di sini
        })
    } else {
        //input nomor salah
    }
})

inputLainLain.onchange = hitungOperasional;
function hitungOperasional() {
    if (stateAutoCalculate) {
        var karyawan = hapusTitik(inputKaryawan.value);
        var listrik = hapusTitik(inputListrik.value);
        var lainlain = hapusTitik(inputLainLain.value);
        totalOperasional = karyawan + listrik + lainlain;
        inputListrik.value = formatRupiah(listrik);
        inputLainLain.value = formatRupiah(lainlain);
        inputOperasional.value = formatRupiah(totalOperasional);
    }
}
setInterval(hitungOperasional, 2000);

inputLainLain.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        hitungOperasional();
    }
});

btnReset.addEventListener('click', function () {
    location.reload();
})