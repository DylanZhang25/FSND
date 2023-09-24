// actorManagementHandler.js

import { initializeAssignActorToMovie, assignActorToMovie } from './assignActorToMovieHandler.js';
import { renderMovieList } from './moviesRenderHandler.js';

const element = layui.element;
const layer = layui.layer;
const $ = layui.$;
const table = layui.table;
const form = layui.form;
let renderActorTable;

// Listening for clicks on the left navigation menu items.
element.on('nav(left_nav)', function (elem){
    const event = elem.attr('data-event'); // Get the name of left navigation menu item.

    // Execute the corresponding action according to the menu item name.
    switch (event) {
        case 'manage_actors':
            $('#introduction-div').hide()
            $('#movie-list-div').hide();
            $('#actor-table-div').show();
            renderActorTable(); // Rendering the actor form
            $('#movies-pagination-container').hide();
            break;
        case 'add_new_actor':
            window.add();
            $('#movies-pagination-container').hide();
            break;
        case 'manage_movies':
            console.log("Manage movies clicked");
            $('#introduction-div').hide();
            $('#actor-table-div').hide();
            $('#movie-list-div').show();
            renderMovieList(1); // Rendering the movies list
            $('#movies-pagination-container').show();
            break;
    }
});

layui.use(['element', 'layer', 'util'], function(){
    // Functions for Rendering Actor Forms
    renderActorTable  = function renderActorTable() {
        const accessToken = sessionStorage.getItem('access_token');
        // data rendering for the actor info table
        const table_instance = table.render({
            elem: '#actor',
            id: 'actor',
            url: '/api/actors',
            toolbar: '#toolbar',
            headers: {
                Authorization: `Bearer ${accessToken}`
            },
            cols: [
                [
                    {field: 'id', title: 'ID', sort: true},
                    {field: 'name', title: 'NAME'},
                    {field: 'age', title: 'AGE'},
                    {field: 'is_time_available', title: 'TIME-FREE'},
                    {field: 'create_at', title: 'CREATE AT'},
                    {field: 'update_at', title: 'UPDATE AT'},
                    {
                        field: 'movies',
                        title: 'WILL ACT IN',
                        width: '30%',
                        templet: function (d) {
                            let movieString = '';
                            layui.each(d.movies, function (index, movie) {
                            movieString += '<span class="layui-badge layui-bg-orange" style="margin-right: 10px;">' + movie + '</span>';
                            });
                            return movieString;
                        }
                    },
                    {title: 'ACTION', width: 250, templet: '#tools'}
                ]
            ],
            page: true,
            limit: 10,
            limits: [10]
        });
    }

    // Search box events in the Actor table
    form.on('submit(table-search)', function (data) {
        const field = data.field; // 获得表单字段
        // 执行搜索重载
        table.reload('actor', {
            page: {
                curr: 1, // Starting from page 1
            },
            where: field,
        });
        return false; // Blocking default form jumps
    });

    // Open a new actor form (actor_add/html) for adding an actor.
    window.add = function () {
        layer.open({
            type: 2,
            title: 'Add an actor',
            shadeClose: true,
            maxmin: true,
            area: ['500px', '400px'],
            content: '/actor_add'
        });
    }

    // Button events in the Actor table.
    table.on('tool(actor)', function (obj) {
        const options = obj.config; // Gets the current table property configuration.
        const checkStatus = table.checkStatus(options.id); // Obtain data about the selected row.

        // Perform operations based on different event names
        switch (obj.event) { // The value of the lay-event attribute in the template element.
            case 'edit_an_actor':
                // Call the window.add() function to open a new actor form
                localStorage.setItem('actorDataFromEditing', JSON.stringify(obj.data));
                window.edit();
                break;
            case 'delete_an_actor':
                // Call the window's delete function to show a confirmation message.
                layer.confirm('Are you sure?', {
                        title: 'Warning',
                        btn: ['Confirm', 'Cancel']
                    }, function (index) {
                        layer.close(index);
                        window.delete_one(obj);
                        }
                );
                break;
            case 'assign_an_actor_to_a_movie':
                // Save the actor's ID to localStorage for later use.
                localStorage.setItem('actorDataFromAssigning', JSON.stringify(obj.data));
                assignActorToMovie()
                break;
        }
    });

    // Function to open a new actor form for adding
    window.edit = function () {
        layer.open({
            type: 2,
            title: 'Edit an actor',
            shadeClose: true,
            maxmin: true,
            area: ['500px', '400px'],
            content: '/actor_edit'
        });
    }

    // Front-end methods for communicating with back-end endpoint
    // `/api/actor/${id}` method: 'DELETE'
    const del_actor_api = async (id) => {
        const token = sessionStorage.getItem('access_token');
        const options = {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
        }
        const response = await fetch(`/api/actor/${id}`, options)
        return await response.json()
    }
    window.delete_one = function (obj) {
        // console.log(obj)
        del_actor_api(obj.data.id).then(function (ret) {
            if (!ret.code) {
                layer.msg(ret.msg, {
                    icon: 1,
                    time: 1000,
                }, function () {
                    table.reload('actor');
                });
            } else {
                layer.msg(ret.msg, {
                    icon: 2,
                    time: 1000,
                });
            }
        })
    }
});

export { renderActorTable };