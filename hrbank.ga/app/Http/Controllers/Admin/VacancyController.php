<?php


namespace App\Http\Controllers\Admin;


use App\Http\Controllers\Controller;
use App\Status;
use App\Vacancy;

class VacancyController extends Controller
{
    public function index()
    {
        $statuses = Status::orderBy('position')->get();
        $vacancies = Vacancy::get();
        return view('admin.vacancies.index', compact('statuses', 'vacancies'));
    }
}