$(document).ready(function) {


    var deleteBtn = $('delete-btn');
    var searchBtn = $('#search-btn');
    var searchForm = $('#search-form');

    $(deleteBtn).on('click', function(e) {

    e.preventDefault();

    var delLink = $(this).attr('href');
    var result = confirm('Deletar esta tarefa');

    if(result) {
        window.location.href = delLink;

    }

    }),

    $(searchBtn).on('click'. function() {
        searchForm.submit();


    }) ;


.vertical-center {
  min-height: 100%;
  min-height: 100vh;
  display: flex;
  align-items: center;
  position: absolute;
  width: 100%;
  top: 0;
}

form {
  border-radius: 15px 15px 15px 15px;
  padding: 25px;
  text-align: center;
  background-color: rgba(237, 237, 237, 0.5);
  background-color: hsla(0, 0%, 93%, 0.5);
  width: 500px;
}

#carousel-img {
  height: 100vh;
  width: 100%;
}

function cloneMore(selector, type) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + type + '-TOTAL_FORMS').val();
    newElement.find(':input').each(function() {
        var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    newElement.find('label').each(function() {
        var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
        $(this).attr('for', newFor);
    });
    total++;
    $('#id_' + type + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
}