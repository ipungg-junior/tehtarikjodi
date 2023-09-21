
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
const btnSimpan = document.getElementById('btn-simpan');

var gajiKaryawan = 0;
var biayaListrik = 0;
var biayaLain = 0;
var hargaPcup = 10000;
var totalOperasional = 0;
var bep = 0;
var labaBersih = 0;
var labaKotor = 0;

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

inputSewaBangunan.onchange = totalBep;

// Tambahkan event listener untuk mengubah kelas saat tombol diklik
function totalBep() {
    var sewabangunan = parseInt((inputSewaBangunan.value).replace(/\./g, ""), 10);
    labaBersih = labaKotor - (totalOperasional)
    outputlaba.textContent = formatRupiah(labaBersih);
    // Hitung BEP
    bep = Math.round((14500000 + sewabangunan) / labaBersih);
    inputSewaBangunan.value = formatRupiah(inputSewaBangunan.value);
    groupLabaBersih.classList.remove('hide');
    groupBEP.classList.remove('hide');
    btnBEP.textContent = bep + " Bulan";
}

// Bussiness Logic Function
inputJumlahHari.addEventListener('change', function () {
    groupOmset.classList.remove('hide');
    groupHpp.classList.remove('hide');
    groupLabaKotor.classList.remove('hide');
    var omsetKotor = 0;
    var hpp = 0;
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


inputLainLain.onchange = hitungOperasional;

function hitungOperasional() {
    var karyawan = hapusTitik(inputKaryawan.value);
    var listrik = hapusTitik(inputListrik.value);
    var lainlain = hapusTitik(inputLainLain.value);
    totalOperasional = karyawan + listrik + lainlain;
    inputListrik.value = formatRupiah(listrik);
    inputLainLain.value = formatRupiah(lainlain);
    inputOperasional.value = formatRupiah(totalOperasional);
    groupOperasional.classList.remove('hide');
}

inputLainLain.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        hitungOperasional();
    }
});

btnReset.addEventListener('click', function () {
    location.reload();
})