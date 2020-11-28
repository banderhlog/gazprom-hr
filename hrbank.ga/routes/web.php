<?php

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});

Auth::routes(['register' => false, 'reset', 'confirm' => false, 'verify' => false]);

Route::get('/home', 'HomeController@index')->name('home');


Route::prefix('')->middleware('auth')->name('admin.')->namespace('Admin')->group(function (){
//    Route::get('/', 'DashboardController@index')->name('dashboard.index');

    Route::prefix('positions')->name('positions.')->group(function (){
        Route::get('/', 'PositionController@index')->name('index');
        Route::get('/add', 'PositionController@add')->name('add');
        Route::get('/{position_id}', 'PositionController@edit')->name('edit');

        Route::post('/', 'PositionController@create')->name('create');
        Route::post('/{position_id}', 'PositionController@update')->name('update');
        Route::delete('/{position_id}', 'PositionController@delete')->name('delete');
    });
});

