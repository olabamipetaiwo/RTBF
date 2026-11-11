# Reardon, Basin, Capkun. SoK: Secure Data Deletion

IEEE S&P 2013, pp. 301-315 (begins on page 301), DOI 10.1109/SP.2013.28. File: `1_systems/reardon-sp13-sok-secure-deletion.pdf`. Read the abstract, introduction, the layers discussion (Section II), the case study of user-level tools on file systems (Section V, Table III) and the conclusions. I did not read the adversary and property taxonomies (Sections III and IV) line by line.

## Question
How can data be deleted so that an adversary with some access to the system cannot recover it, and which approaches achieve that at which layer of a storage system (Abstract, Section I)?

## Definition and scope
- "Data is securely deleted from a system if an adversary that is given some manner of access to the system is not able to recover the deleted data from the system" (Section I).
- The scope is data the owner can address by a handle (file name, database record). It explicitly excludes deleting "all copies of some information" and "all derivative works of data" (Section I).
- Lists many names for the same idea (forgotten, erased, purged, self-destructed, sanitized, revoked, destroyed), showing the vocabulary is not settled (Section I).

## Main argument
- Users delete to recover storage, not to make data irrecoverable, yet browsers label clearing history a privacy option and users "typically assume, falsely, that when they delete the data, it is from that moment on irrecoverable" (Section I).
- Every file system "deletes" by unlinking: the metadata changes, the content stays (Section I).
- The layer trade-off (Section II): at the physical layer deletion can be made truly irrecoverable; at the user layer the data object is easy to identify. "The further one's interface is abstracted away from the physical medium, the more difficult it is to ensure that one's actions truly result in the irrecoverability of data."

## Experiments (Section V, Table III)
- Tested user-level tools (overwriting tools such as shred, srm, wipe, and "filling" the free space) on several file systems, including truncation, sparse files and metadata.
- Overwriting works only on simple file systems; journalling, log-structured and copy-on-write file systems leave old data. File renaming rarely removed the old name in any file system tested. No file system sanitized entirely discarded blocks after truncation. Some tools reported success while the data remained (for example srm and wipe on a sparse file exceeding the file system).
- Conclusion: "user-level approaches are generally limited and cannot securely delete data in all cases"; filling is often preferable to overwriting, but it works only under environmental assumptions that deployed systems often do not meet.

## How it differs from ours
- It covers storage media and file systems, not services or agents, and a handle-addressable object, not facts extracted into memory.
- Its method is to test what remains after a deletion operation, which is the same logic as our recall check. Its finding that a successful-looking delete can leave the data readable, and that tools can report success anyway, parallels our result that agents reply that they complied while the fact remains.

## Use in our paper
- Strong background for "deleting at the interface the user sees does not guarantee removal at the layers below" (Section 6.1, Discussion) and for the point that users assume deletion is irrecoverable. Cite for the layering argument and for the definition of secure deletion.
- Note the scope exclusion: this definition does not cover derived data, which is where agent memory sits. Cao and Yang (S&P 2015) and the unlearning papers cover that gap.
- Vanish, cited in this paper's reference list as USENIX Security 2009, pp. 299-316; compare with the page range in the Vanish note.
