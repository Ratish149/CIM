# Startup & Entrepreneurship Pavilion (BIC) — Frontend Integration Guide

This guide details how to integrate the **Startup & Entrepreneurship Pavilion Enquiry Form** (Birat Expo 2026 · Biratnagar Incubation Center) in your Next.js / TypeScript frontend using **TanStack Query**.

---

## 1. API Endpoint Overview

- **URL:** `/api/startup/registrations/`
- **Method:** `POST`
- **Authentication:** None (Public / `AllowAny`)
- **Content-Type:** `application/json`

### Success Response (`201 Created`):
```json
{
  "id": 1,
  "track": "Makerspace",
  "status": "Pending",
  "full_name": "Ram Bahadur",
  "phone": "9841234567",
  "email": "ram@school.edu.np",
  "organization_name": "Adarsha Secondary School",
  "role": "Principal",
  "municipality": "Biratnagar, Morang",
  "notes": "Wheelchair access needed for 2 students.",
  "school_request": "Class visit to Room 1 at Birat Expo",
  "school_type": "Community (government)",
  "school_grades": "7, 8, 9",
  "school_students_count": 30,
  "school_teachers_count": 2,
  "school_preferred_date_1": "Thu 17 Dec (2 Poush)",
  "school_preferred_date_2": "Fri 18 Dec (3 Poush)",
  "school_session_slot": "Morning",
  "school_session_month": null,
  "school_available_space": null,
  "gender": null,
  "age_group": null,
  "college_programme": null,
  "college_year": null,
  "idea_stage": null,
  "interested_topics": null,
  "preferred_contact_channel": null,
  "willing_to_host_workshop": false,
  "district": null,
  "business_registration_type": null,
  "trading_duration": null,
  "business_sector": null,
  "employees_count": null,
  "annual_turnover": null,
  "ownership_diversity": null,
  "area_of_interest": null,
  "expo_visit_day": null,
  "support_needs": null,
  "biggest_challenge": null,
  "heard_about_us": "CIM website",
  "consent": true,
  "keep_updated": true,
  "created_at": "2026-11-04T07:35:00.000000Z",
  "updated_at": "2026-11-04T07:35:00.000000Z"
}
```

---

## 2. TypeScript Types (`types/startupRegistration.ts`)

```typescript
export type TrackType = "Makerspace" | "Design Studio" | "Growth Room";

export type LegacyTrackKey = "school" | "college" | "business";

export type RegistrationStatus =
  | "Pending"
  | "Contacted"
  | "Confirmed"
  | "Completed"
  | "Cancelled";

export type HeardAboutUsChoice =
  | "At Birat Expo"
  | "CIM website"
  | "Facebook / social media"
  | "School / college"
  | "Friend or colleague"
  | "CIM member / staff"
  | "Newspaper / radio"
  | "Other";

// Base interface with common fields
export interface BaseRegistrationPayload {
  track: TrackType | LegacyTrackKey;
  full_name: string;
  phone: string;
  email?: string | null;
  organization_name?: string | null;
  role?: string | null;
  municipality?: string | null;
  notes?: string | null;
  heard_about_us?: HeardAboutUsChoice | string | null;
  consent: boolean;
  keep_updated?: boolean;
}

// Room 1: Makerspace (Schools & Teachers)
export interface MakerspaceRegistrationPayload extends BaseRegistrationPayload {
  track: "Makerspace" | "school";
  school_request: string;
  school_type?: string | null;
  school_grades: string; // e.g. "7, 8, 9, 10"
  school_students_count: number;
  school_teachers_count?: number | null;
  school_preferred_date_1?: string | null;
  school_preferred_date_2?: string | null;
  school_session_slot?: "Morning" | "Afternoon" | "Either" | string | null;
  school_session_month?: string | null;
  school_available_space?: string | null;
}

// Room 2: Design Studio (College Students)
export interface DesignStudioRegistrationPayload extends BaseRegistrationPayload {
  track: "Design Studio" | "college";
  college_programme: string; // e.g. "BBS, BBA, BSc CSIT"
  college_year?: string | null;
  gender?: "Female" | "Male" | "Other" | "Prefer not to say" | string | null;
  age_group?: "Under 18" | "18–21" | "22–25" | "26–30" | "Over 30" | string | null;
  idea_stage: string; // e.g. "No idea yet, just curious"
  interested_topics?: string | null; // e.g. "Agriculture & food, Tech & digital"
  preferred_contact_channel: "Phone call" | "SMS" | "Viber / WhatsApp" | "Email" | string;
  willing_to_host_workshop?: boolean;
}

// Room 3: Growth Room (Business Owners)
export interface GrowthRoomRegistrationPayload extends BaseRegistrationPayload {
  track: "Growth Room" | "business";
  district: string; // e.g. "Morang", "Sunsari", "Outside Koshi Province"
  business_registration_type: string; // e.g. "Company (OCR)"
  trading_duration: string; // e.g. "1–3 years"
  business_sector: string; // e.g. "Agriculture & agro-processing"
  employees_count?: "1–4" | "5–9" | "10–19" | "20–49" | "50+" | string | null;
  annual_turnover?: string | null;
  ownership_diversity?: string | null; // e.g. "Women-led, Youth-led (under 40)"
  area_of_interest: string; // e.g. "Health Check-up + SGB Accelerator"
  expo_visit_day?: string | null;
  support_needs?: string | null; // e.g. "Finance & loans, Marketing & branding"
  biggest_challenge?: string | null;
}

export type StartupRegistrationPayload =
  | MakerspaceRegistrationPayload
  | DesignStudioRegistrationPayload
  | GrowthRoomRegistrationPayload;

export interface StartupRegistrationResponse {
  id: number;
  track: TrackType;
  status: RegistrationStatus;
  full_name: string;
  phone: string;
  email: string | null;
  organization_name: string | null;
  role: string | null;
  municipality: string | null;
  notes: string | null;
  school_request: string | null;
  school_type: string | null;
  school_grades: string | null;
  school_students_count: number | null;
  school_teachers_count: number | null;
  school_preferred_date_1: string | null;
  school_preferred_date_2: string | null;
  school_session_slot: string | null;
  school_session_month: string | null;
  school_available_space: string | null;
  gender: string | null;
  age_group: string | null;
  college_programme: string | null;
  college_year: string | null;
  idea_stage: string | null;
  interested_topics: string | null;
  preferred_contact_channel: string | null;
  willing_to_host_workshop: boolean;
  district: string | null;
  business_registration_type: string | null;
  trading_duration: string | null;
  business_sector: string | null;
  employees_count: string | null;
  annual_turnover: string | null;
  ownership_diversity: string | null;
  area_of_interest: string | null;
  expo_visit_day: string | null;
  support_needs: string | null;
  biggest_challenge: string | null;
  heard_about_us: string | null;
  consent: boolean;
  keep_updated: boolean;
  created_at: string;
  updated_at: string;
}
```

---

## 3. Dedicated API Function (`api/startupRegistration.ts`)

```typescript
import {
  StartupRegistrationPayload,
  StartupRegistrationResponse,
} from "@/types/startupRegistration";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "https://cim.baliyoventures.com";

export async function createStartupRegistration(
  payload: StartupRegistrationPayload
): Promise<StartupRegistrationResponse> {
  const response = await fetch(`${API_BASE_URL}/api/startup/registrations/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(
      errorData?.detail ||
        (errorData ? JSON.stringify(errorData) : "Failed to submit enquiry.")
    );
  }

  return response.json();
}
```

---

## 4. TanStack Query Mutation Hook (`hooks/useCreateStartupRegistration.ts`)

```typescript
import { useMutation } from "@tanstack/react-query";
import { createStartupRegistration } from "@/api/startupRegistration";
import {
  StartupRegistrationPayload,
  StartupRegistrationResponse,
} from "@/types/startupRegistration";

interface UseCreateStartupRegistrationOptions {
  onSuccess?: (data: StartupRegistrationResponse) => void;
  onError?: (error: Error) => void;
}

export function useCreateStartupRegistration(
  options?: UseCreateStartupRegistrationOptions
) {
  return useMutation({
    mutationFn: (payload: StartupRegistrationPayload) =>
      createStartupRegistration(payload),
    onSuccess: (data) => {
      options?.onSuccess?.(data);
    },
    onError: (error: Error) => {
      options?.onError?.(error);
    },
  });
}
```

---

## 5. Sample Payloads by Track

### Track 1: Makerspace (Schools & Teachers)
```json
{
  "track": "Makerspace",
  "full_name": "Ramesh Karki",
  "phone": "9842012345",
  "email": "info@adarshaschool.edu.np",
  "organization_name": "Shree Adarsha Secondary School",
  "role": "Principal",
  "municipality": "Biratnagar-3, Morang",
  "school_request": "Class visit to Room 1 at Birat Expo",
  "school_type": "Community (government)",
  "school_grades": "7, 8, 9",
  "school_students_count": 35,
  "school_teachers_count": 2,
  "school_preferred_date_1": "Thu 17 Dec (2 Poush)",
  "school_preferred_date_2": "Fri 18 Dec (3 Poush)",
  "school_session_slot": "Morning",
  "notes": "Please arrange entry passes for two school staff.",
  "heard_about_us": "CIM website",
  "consent": true,
  "keep_updated": true
}
```

### Track 2: Design Studio (College Students)
```json
{
  "track": "Design Studio",
  "full_name": "Pooja Sharma",
  "phone": "9812345678",
  "email": "pooja.sharma@gmail.com",
  "organization_name": "Mahendra Morang Adarsha Multiple Campus",
  "college_programme": "BSc CSIT",
  "college_year": "3rd year",
  "gender": "Female",
  "age_group": "18–21",
  "municipality": "Biratnagar",
  "idea_stage": "I have a rough idea",
  "interested_topics": "Tech & digital, Agriculture & food",
  "preferred_contact_channel": "Viber / WhatsApp",
  "willing_to_host_workshop": true,
  "notes": "Would love to coordinate with our student IT club.",
  "heard_about_us": "Facebook / social media",
  "consent": true,
  "keep_updated": true
}
```

### Track 3: Growth Room (Business Owners)
```json
{
  "track": "Growth Room",
  "full_name": "Bijay Shrestha",
  "phone": "9852023456",
  "email": "bijay@koshipackaging.com",
  "organization_name": "Koshi Packaging Industries Pvt. Ltd.",
  "role": "Owner / founder",
  "district": "Morang",
  "municipality": "Biratnagar",
  "business_registration_type": "Company (OCR)",
  "trading_duration": "3–5 years",
  "business_sector": "Manufacturing",
  "employees_count": "10–19",
  "annual_turnover": "NPR 1–5 crore",
  "ownership_diversity": "Youth-led (under 40)",
  "area_of_interest": "Health Check-up + SGB Accelerator",
  "expo_visit_day": "Sat 19 Dec (4 Poush)",
  "support_needs": "Access to finance / loans, Packaging & product quality, Market linkage",
  "biggest_challenge": "Scaling production machinery and working capital financing.",
  "notes": "Looking forward to meeting growth advisors.",
  "heard_about_us": "At Birat Expo",
  "consent": true,
  "keep_updated": false
}
```

---

## 6. Full Form Component Example (`components/BicPavilionForm.tsx`)

```tsx
"use client";

import React, { useState } from "react";
import { useCreateStartupRegistration } from "@/hooks/useCreateStartupRegistration";
import {
  TrackType,
  StartupRegistrationPayload,
  StartupRegistrationResponse,
} from "@/types/startupRegistration";

export default function BicPavilionForm() {
  const [selectedTrack, setSelectedTrack] = useState<TrackType>("Makerspace");
  const [submittedData, setSubmittedData] =
    useState<StartupRegistrationResponse | null>(null);

  // Common fields
  const [fullName, setFullName] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [organizationName, setOrganizationName] = useState("");
  const [role, setRole] = useState("");
  const [municipality, setMunicipality] = useState("");
  const [notes, setNotes] = useState("");
  const [heardAboutUs, setHeardAboutUs] = useState("At Birat Expo");
  const [consent, setConsent] = useState(false);
  const [keepUpdated, setKeepUpdated] = useState(true);

  // Makerspace specific
  const [schoolRequest, setSchoolRequest] = useState("Class visit to Room 1 at Birat Expo");
  const [schoolGrades, setSchoolGrades] = useState<string[]>(["7", "8"]);
  const [studentCount, setStudentCount] = useState<number>(30);

  // Design Studio specific
  const [collegeProgramme, setCollegeProgramme] = useState("");
  const [ideaStage, setIdeaStage] = useState("I have a rough idea");
  const [contactChannel, setContactChannel] = useState("Phone call");

  // Growth Room specific
  const [district, setDistrict] = useState("Morang");
  const [businessReg, setBusinessReg] = useState("Company (OCR)");
  const [tradingDuration, setTradingDuration] = useState("1–3 years");
  const [businessSector, setBusinessSector] = useState("Manufacturing");
  const [areaOfInterest, setAreaOfInterest] = useState("Health Check-up + SGB Accelerator");

  const { mutate, isPending, error } = useCreateStartupRegistration({
    onSuccess: (data) => {
      setSubmittedData(data);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    let payload: StartupRegistrationPayload;

    if (selectedTrack === "Makerspace") {
      payload = {
        track: "Makerspace",
        full_name: fullName,
        phone,
        email: email || null,
        organization_name: organizationName,
        role: role || "Teacher",
        municipality,
        school_request: schoolRequest,
        school_grades: schoolGrades.join(", "),
        school_students_count: Number(studentCount),
        notes: notes || null,
        heard_about_us: heardAboutUs,
        consent,
        keep_updated: keepUpdated,
      };
    } else if (selectedTrack === "Design Studio") {
      payload = {
        track: "Design Studio",
        full_name: fullName,
        phone,
        email: email || null,
        organization_name: organizationName,
        college_programme: collegeProgramme,
        idea_stage: ideaStage,
        preferred_contact_channel: contactChannel,
        municipality,
        notes: notes || null,
        heard_about_us: heardAboutUs,
        consent,
        keep_updated: keepUpdated,
      };
    } else {
      payload = {
        track: "Growth Room",
        full_name: fullName,
        phone,
        email: email || null,
        organization_name: organizationName,
        role: role || "Owner / founder",
        district,
        municipality,
        business_registration_type: businessReg,
        trading_duration: tradingDuration,
        business_sector: businessSector,
        area_of_interest: areaOfInterest,
        notes: notes || null,
        heard_about_us: heardAboutUs,
        consent,
        keep_updated: keepUpdated,
      };
    }

    mutate(payload);
  };

  if (submittedData) {
    return (
      <div className="max-w-xl mx-auto p-8 bg-white border border-slate-200 rounded-xl shadow-sm text-center">
        <div className="w-16 h-16 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto text-3xl font-bold mb-4">
          ✓
        </div>
        <h2 className="text-2xl font-bold text-slate-900">
          Enquiry Received, {submittedData.full_name}!
        </h2>
        <p className="text-sm text-slate-600 mt-2">
          Thank you for reaching out. We have sent a confirmation email to{" "}
          <strong>{submittedData.email || submittedData.phone}</strong>.
        </p>
        <button
          onClick={() => setSubmittedData(null)}
          className="mt-6 text-sm text-blue-600 underline font-medium"
        >
          Submit another enquiry
        </button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="max-w-2xl mx-auto p-6 bg-white border border-slate-200 rounded-xl space-y-6">
      <div>
        <h2 className="text-xl font-bold text-slate-900">
          Startup &amp; Entrepreneurship Pavilion
        </h2>
        <p className="text-sm text-slate-500">
          Birat Expo 2026 · Biratnagar Incubation Center (CIM)
        </p>
      </div>

      {/* Step 1: Choose Track */}
      <div>
        <label className="block text-sm font-semibold text-slate-700 mb-2">
          Select Your Category
        </label>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {(["Makerspace", "Design Studio", "Growth Room"] as TrackType[]).map((t) => (
            <button
              key={t}
              type="button"
              onClick={() => setSelectedTrack(t)}
              className={`p-3 rounded-lg border text-left text-sm font-medium transition ${
                selectedTrack === t
                  ? "border-blue-600 bg-blue-50 text-blue-900"
                  : "border-slate-200 hover:bg-slate-50 text-slate-700"
              }`}
            >
              {t === "Makerspace" && "Room 1: Schools (Makerspace)"}
              {t === "Design Studio" && "Room 2: College Students"}
              {t === "Growth Room" && "Room 3: Business Owners"}
            </button>
          ))}
        </div>
      </div>

      {/* Contact Fields */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label className="block text-xs font-semibold text-slate-600 mb-1">
            Full Name *
          </label>
          <input
            type="text"
            required
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm"
            placeholder="e.g. Ramesh Karki"
          />
        </div>
        <div>
          <label className="block text-xs font-semibold text-slate-600 mb-1">
            Mobile Number *
          </label>
          <input
            type="tel"
            required
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm"
            placeholder="98XXXXXXXX"
          />
        </div>
        <div>
          <label className="block text-xs font-semibold text-slate-600 mb-1">
            Email Address
          </label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm"
            placeholder="name@example.com"
          />
        </div>
        <div>
          <label className="block text-xs font-semibold text-slate-600 mb-1">
            {selectedTrack === "Makerspace"
              ? "School Name *"
              : selectedTrack === "Design Studio"
              ? "College Name *"
              : "Business Name *"}
          </label>
          <input
            type="text"
            required
            value={organizationName}
            onChange={(e) => setOrganizationName(e.target.value)}
            className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm"
          />
        </div>
      </div>

      {/* Consent & Submit */}
      <div className="space-y-2 pt-2 border-t border-slate-100">
        <label className="flex items-start gap-2 text-xs text-slate-600 cursor-pointer">
          <input
            type="checkbox"
            required
            checked={consent}
            onChange={(e) => setConsent(e.target.checked)}
            className="mt-0.5"
          />
          <span>
            I agree that Biratnagar Incubation Center and CIM may contact me regarding this enquiry. *
          </span>
        </label>
        <label className="flex items-start gap-2 text-xs text-slate-600 cursor-pointer">
          <input
            type="checkbox"
            checked={keepUpdated}
            onChange={(e) => setKeepUpdated(e.target.checked)}
            className="mt-0.5"
          />
          <span>Keep me updated about other CIM entrepreneurship initiatives.</span>
        </label>
      </div>

      {error && (
        <div className="text-xs text-rose-600 bg-rose-50 p-2.5 rounded border border-rose-200">
          {error.message}
        </div>
      )}

      <button
        type="submit"
        disabled={isPending}
        className="w-full py-3 bg-blue-700 hover:bg-blue-800 disabled:opacity-50 text-white font-semibold rounded-lg text-sm transition"
      >
        {isPending ? "Submitting enquiry..." : "Submit Enquiry"}
      </button>
    </form>
  );
}
```

---

## 7. Key Rules & Notes for Frontend Engineers

1. **Automated Emails:** Whenever an enquiry is posted with an `email` field, the backend automatically dispatches:
   - An HTML confirmation email to the user with details about their selected room and next steps.
   - An HTML admin alert to `ADMIN_EMAIL`.
2. **Flexible Track Formats:** The backend accepts both `"Makerspace"` / `"Design Studio"` / `"Growth Room"` and legacy HTML radio values `"school"` / `"college"` / `"business"`.
