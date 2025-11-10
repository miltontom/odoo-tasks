$(document).ready(function () {
    $("#back-btn").hide()
    $("#candidates-table-readonly").hide()
    $("#end-vote-btn").hide()
    $("#multiselect-delete-btn").hide()

    let candidates = {}
    class Candidate {
        constructor(name, id) {
            this.name = name
            this.id = id
            this.voteCount = 0
        }
    }

    $("#id-field").keypress(function (e) {
        let key = e.keyCode

        if (key == 13) {
            $("#add-btn").trigger('click')
        }
    })

    $("#add-btn").click(function () {
        let candName = $("#name-field").val()
        let candId = $("#id-field").val()

        if (candId === "" || candName === "") {
            $("#empty-field-modal").modal('show')
            $("#name-field").val('')
            $("#id-field").val('')
            $("#name-field").focus()
            return
        }

        if (candId in candidates) {
            $("#duplicate-id-modal").modal('show')
            $("#name-field").val('')
            $("#id-field").val('')
            $("#name-field").focus()
            return
        }

        candidates[candId] = new Candidate(candName, candId)

        let newRow = `
            <tr id="row-${candId}">
                <td><input class="subcheckbox" id="single-checkbox" type="checkbox"></td>
                <td id="id-cell">${candId}</td>
                <td id="name-cell">${candName}</td>
                <td><button id="edit-btn">Edit</button></td>
                <td><button id="delete-btn">Delete</button></td>
            </tr>
        `
        $("#candidates-table").find('tbody').append(newRow)
        $("#name-field").val('')
        $("#id-field").val('')
        $("#name-field").focus()
    })

    $(document).on('click', '#delete-btn', function () {
        let row = $(this).closest('tr')
        let id = row.attr('id').split('-')[1]
        delete candidates[id]
        row.remove()
    })

    $("#candidates-table").on('click', '#edit-btn', function () {
        let row = $(this).closest('tr')
        let prevId = row.find('#id-cell').text()
        let prevName = row.find('#name-cell').text()

        row.find('#id-cell').html(`<input id="temp-id-field" type="text" value=${prevId}>`)
        row.find('#name-cell').html(`<input id="temp-name-field" type="text" value=${prevName}>`)
        $(this).text("Save").attr('id', 'save-btn')

    })
    $("#candidates-table").on('click', '#save-btn', function () {
        let row = $(this).closest('tr')

        let newId = row.find('#temp-id-field').val()
        let newName = row.find('#temp-name-field').val()

        let id = row.attr('id').split('-')[1]

        if (newId === id || !(newId in candidates)) {
            row.find('#id-cell').text(newId)
            row.find('#name-cell').text(newName)
        } else {
            $("#duplicate-id-modal").modal('show')
            return
        }

        $(this).text("Edit").attr("id", "edit-btn")
    })

    mulToDelete = []
    toDelete = []
    selectedCount = 0
    $("#candidates-table").on('click', "#single-checkbox", function () {
        let row = $(this).closest('tr')
        let id = row.attr('id').split('-')[1]
        if ($(this).prop("checked")) {
            toDelete.push(id)
            console.log(toDelete)
            selectedCount += 1
            console.log(selectedCount)
        } else {
            toDelete.pop(id)
            mulToDelete.pop(id)
            console.log(toDelete)
            selectedCount -= 1
            console.log(selectedCount)
        }

        if (selectedCount == 0) {
            $("#multiselect-delete-btn").hide()
            selectedCount = 0
        } else {
            $("#multiselect-delete-btn").show()
        }
    })

    $("#select-all").change(function () {
        if ($(this).prop('checked')) {
            $("#multiselect-delete-btn").show()
            $(".subcheckbox:checkbox").prop('disabled', true)
            $(".subcheckbox").prop('checked', true)
            $(".subcheckbox:checkbox").each(function () {
                let rowId = $(this).closest('tr').attr('id').split('-')[1]
                if ($(this).prop("checked")) {
                    mulToDelete.push(rowId)
                    console.log(mulToDelete)
                }
            })
        } else {
            selectedCount = 0
            $("#multiselect-delete-btn").hide()
            $(".subcheckbox:checkbox").prop('disabled', false)
            $(".subcheckbox").prop('checked', false)
            toDelete = []
            console.log(toDelete)
            console.log(selectedCount)
        }
    })

    $("#multiselect-delete-btn").click(function () {
        for (let i = 0; i < toDelete.length; i++) {
            $(`#row-${toDelete[i]}`).remove()
        }
        toDelete = []
        $("#select-all").prop("checked", false)
        console.log(toDelete)
        $(this).hide()
    })

    $("#start-vote-btn").click(function () {
        $("#input-form").hide()
        $("#candidates-table").hide()
        $("#candidates-table-readonly").show()
        $("#back-btn").show()
        $("#end-vote-btn").show()
        $(this).hide()

        $("#candidates-table-readonly").find('tbody').empty()

        for (candId in candidates) {
            let id = candId
            let name = candidates[candId].name
            let row = `
            <tr>
                <td>${id}</td>
                <td>${name}</td>
                <td><button id="vote-btn">Vote</button></td>
            </tr>
            `
            $("#candidates-table-readonly").find('tbody').append(row)
        }
        console.log(candidates)
    })

    $("#candidates-table-readonly").on('click', '#vote-btn', function () {
        let id = $(this).closest('tr').find('td:first').text()
        candidates[id].voteCount += 1
    })

    $(document).on('click', "#end-vote-btn", function () {
        let currMax = -1
        let winner = ''
        for (let id in candidates) {
            let voteCount = candidates[id].voteCount
            if (voteCount > currMax) {
                currMax = voteCount
                winner = candidates[id].name
            }
            console.log(candidates[id].name, candidates[id].voteCount)
        }

        $("#winner-modal").find('.modal-title').text(`Congratulations`)
        $("#winner-modal").find('.modal-body').text(`${winner} won the campaign by ${currMax} votes!`)
        $("#winner-modal").modal('show')

        for (let id in candidates) {
            candidates[id].voteCount = 0
        }
    })

    $("#back-btn").click(function () {
        $("#input-form").show()
        $("#candidates-table").show()
        $("#start-vote-btn").show()
        $(this).hide()
        $("#candidates-table-readonly").hide()
        $("#end-vote-btn").hide()

        // perform other reset
    })
})
