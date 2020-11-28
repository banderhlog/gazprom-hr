@extends('layouts.admin')

@section('title') @endsection

@section('content')
    <div class="container section">
        <div class="row">
            <div class="col-6">
                <div class="section__subtitle">Вакансии</div>
                <div class="section__title">Список вакансий</div>
            </div>

            <div class="col-6 section__btns">
                <button class="btn btn_blue btn_md">Создать вакансию</button>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <tabs items='{{ $statuses }}'></tabs>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <list></list>
            </div>
        </div>
    </div>
@endsection