@extends('layouts.admin')

@section('title') @endsection

@section('content')
    <div class="container section">

        <div class="row">
            <div class="col-12">
                <div class="section__title">Новая должность</div>
            </div>
        </div>

        <div class="row">
            <div class="col-6">
                <div class="row">
                    <div class="col-12">
                        <field-input title="Должность"></field-input>
                    </div>
                </div>
            </div>

            <div class="col-6">
                <div class="preview"></div>
            </div>
        </div>
    </div>
@endsection