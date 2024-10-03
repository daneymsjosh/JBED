<?php

namespace App\Http\Controllers;

use App\Models\Contact;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Storage;
use App\Http\Requests\StoreContactRequest;
use App\Http\Requests\UpdateContactRequest;

class ContactController extends Controller
{
    public function index(Request $request)
    {
        $contacts = Contact::when($request->has('search'), function ($query) {
            $query->search(request('search', ''));
        })->paginate(5);

        return response()->json([
            'message' => 'Contacts Retrieved',
            'data' => $contacts
        ], 200);
    }

    public function upload(StoreContactRequest $request)
    {
        $request->validated();

        $fileName = $request->file('file')->getClientOriginalName();
        $path = $request->file('file')->storeAs('contacts', $fileName);

        // $records = Storage::json($path);

        // foreach ($records as $record) {
        //     Contact::create([
        //         'name' => $record['name'],
        //         'email' => $record['email'],
        //         'phone' => $record['phone'],
        //     ]);
        // }

        return response()->json([
            'message' => 'File Uploaded Successfully',
            'path' => $path
        ], 200);
    }

    public function update(UpdateContactRequest $request, Contact $contact)
    {
        $validated = $request->validated();

        $contact->update($validated);

        return response()->json([
            'message' => 'Contact Updated Successfully',
            'data' => $contact
        ], 200);
    }

    public function destroy(Contact $contact)
    {
        $contact->delete();

        return response()->json([
            'message' => 'Contact Deleted Successfully',
            'data' => $contact
        ], 200);
    }

    public function show(Contact $contact)
    {
        return response()->json([
            'message' => 'Showing Contact',
            'data' => $contact
        ], 200);
    }
}
