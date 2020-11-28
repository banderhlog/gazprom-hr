<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Requirement;

class PositionController extends Controller
{
    public function index()
    {
        return view('admin.positions.index');
    }

    public function add()
    {
        $requirements = Requirement::with('options')->get();
        return view('admin.positions.form', compact('requirements'));
    }
    
    public function edit()
    {
        
    }

    public function create()
    {
        
    }

    public function update()
    {
        
    }
}