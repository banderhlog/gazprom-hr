<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Requirement extends Model
{
    public $timestamps = false;

    public function options()
    {
        return $this->hasMany(Option::class, 'requirement_id', 'id');
    }
}
