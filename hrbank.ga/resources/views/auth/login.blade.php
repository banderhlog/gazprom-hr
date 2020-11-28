@extends('layouts.admin')

@section('content')
    <div class="login-card__wrapper">
        <div class="login-card">
            <form method="POST" action="{{ route('login') }}">
                @csrf
                <field-input title="E-mail" type="email" @error('email') error="{{ $message }}" @enderror></field-input>
                <field-input title="Пароль" type="password" @error('password') error="{{ $message }}" @enderror></field-input>
                <button class="btn btn_blue btn_md" type="button">Войти</button>
            </form>
        </div>
    </div>
@endsection
