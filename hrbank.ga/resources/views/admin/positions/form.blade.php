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
                <div class="row">
                    <div class="col-12">
                        <div class="h2">Требования</div>
                        <div class="subtitle">Составьте список требований для данной должности. В зависимости от выбранного требования, Вы можете дополнить его описанием или смежными с ним компетенциями</div>
                        <div class="row">

{{--                                <field-select options='{{ $requirements }}' title="Требование"></field-select>--}}
                                <requirements req='{{ $requirements }}'></requirements>

{{--                            <div class="col-6">--}}
{{--                                <field-select title="Требование"></field-select>--}}
{{--                            </div>--}}
                        </div>
{{--                        <div class="card">--}}
{{--                            --}}
{{--                        </div>--}}
                    </div>
                </div>
            </div>

            <div class="col-6">
                <div class="preview"></div>
            </div>
        </div>
    </div>
@endsection
<script>
    import Requirements from "../../../js/components/requirements";
    export default {
        components: {Requirements}
    }
</script>