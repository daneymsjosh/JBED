<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class Contact extends Model
{
    use HasFactory;

    protected $fillable = [
        'name',
        'email',
        'phone'
    ];

    public function scopeSearch(Builder $query, $search = '')
    {
        $query->where('name', 'like', '%' . $search . '%')->orWhere('email', 'like', '%' . $search . '%');
    }
}
