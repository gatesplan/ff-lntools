# Information hiding (Parnas) and separation of concerns (Dijkstra): what the original sources say about module boundaries

Tags: [P] = read in the original this session; [P*] = the author's own words, read in the author's slides, abstract or comment rather than the paper; [S] = secondary (reproduction, summary, lecture notes). Evidence kind is given in words. Research date 2026-10-18. Originals I could not reach are listed under Gaps.

## 1. Parnas (1972): the decomposition criterion, the KWIC contrast, and what "module" means

### Takeaway
List the difficult design decisions and those likely to change, and make each module hide one of them. Do not decompose by processing steps (the flowchart). A "module" is a responsibility or work assignment, not a subprogram. The evidence is one worked toy example, class-project experience and an openly subjective judgment. Nothing was measured.

### Cited Findings
- Source: D. L. Parnas, "On the Criteria To Be Used in Decomposing Systems into Modules," *CACM* 15(12):1053–1058, Dec 1972, DOI 10.1145/361598.361623. Read in full [P]: [PDF](https://www.cse.sc.edu/~mgv/csce590f20/ParnasCriteria.pdf). The 1971 CMU tech report version was not compared ([DTIC](https://apps.dtic.mil/sti/tr/pdf/AD0773837.pdf)).
- **Definition of module**: "'module' is considered to be a responsibility assignment rather than a subprogram. The modularizations include the design decisions which must be made before the work on independent modules can begin." The aim is to describe all "'system level' decisions (i.e. decisions which affect more than one module)" [P]. [Parnas 1972](https://www.cse.sc.edu/~mgv/csce590f20/ParnasCriteria.pdf)
- **Expected benefits** (expectations, not measurements) [P]:
  - "(1) managerial—development time should be shortened because separate groups would work on each module with little need for communication"
  - "(2) product flexibility—it should be possible to make drastic changes to one module without a need to change others"
  - "(3) comprehensibility—it should be possible to study the system one module at a time"
- **The KWIC example**: the index takes lines, circularly shifts each one, and outputs "all circular shifts of all lines in alphabetical order". Parnas admits a good programmer could build it "within a week or two", so "we must go through the exercise of treating this problem as if it were a large project" [P].
  - **Decomposition 1 (processing steps)**: Input, Circular Shift, Alphabetizing, Output, Master Control. The interfaces are shared core formats. Parnas says "Experiments on a small scale" suggest most programmers would propose this split, but the experiments are not described.
  - **Decomposition 2**: Line Storage (CHAR/SETCHAR/WORDS…), Input, Circular Shifter, Alphabetizer (ALPH/ITH), Output, Master Control. [Parnas 1972](https://www.cse.sc.edu/~mgv/csce590f20/ParnasCriteria.pdf)
- **The difference is not in the code that runs** (argument): the two "could conceivably be identical after assembly". "The differences... are in the way that they are divided into the work assignments, and the interfaces between modules... other representations are used for changing, documenting, understanding" [P].
- **Changeability** (thought experiment, no measurement): Parnas lists five decisions "likely to change": the input format, keeping all lines in core, packing four characters to a word, indexing the shifts instead of storing them, and alphabetizing once.
  - In decomposition 1, the core and packing changes "would result in changes in every module!"
  - In decomposition 2, "Knowledge of the exact way that the lines are stored is entirely hidden from all but module 1."
  - In decomposition 2, the alphabetizer was built so "a user could not detect when the alphabetization was actually done" [P].
- **Independent development and comprehensibility** [P]:
  - Decomposition 1's interfaces are "fairly complex formats and table organizations" that need "a joint effort among the several development groups".
  - Decomposition 2's interfaces "consist primarily in the function names and the numbers and types of the parameters". Parnas later disowns this signature view (§3).
  - Decomposition 1 "will only be comprehensible as a whole. It is my subjective judgment that this is not true in the second" (opinion).
- **The criterion**: decomposition 1 makes "each major step in the processing a module... one makes a flowchart". The flowchart was "useful... for systems with on the order of 5,000-10,000 instructions". Decomposition 2 used "'information hiding' [4] as a criterion... Every module... is characterized by its knowledge of a design decision which it hides from all others. Its interface or definition was chosen to reveal as little as possible about its inner workings." Ref. [4] is the 1971 IFIP paper [P]. [Parnas 1972](https://www.cse.sc.edu/~mgv/csce590f20/ParnasCriteria.pdf)
- **Self-critique**: fixing the order of the shifts "given more information than necessary and so unnecessarily restricted the class of systems that we can build without changing the definitions... must clearly be classified as a design error" [P].
- **Five specific rules** (heuristics from experience) [P]:
  1. "A data structure, its internal linkings, accessing procedures and modifying procedures are part of a single module. They are not shared by many modules as is conventionally done."
  2. The calling sequence of a routine belongs to the same module as the routine.
  3. Control-block formats "must be hidden within a 'control block module'", even though "It is conventional to make such formats the interfaces between various modules".
  4. "Character codes, alphabetic orderings, and similar data should be hidden".
  5. "The sequence in which certain items will be processed should (as far as practical) be hidden within a single module." [Parnas 1972](https://www.cse.sc.edu/~mgv/csce590f20/ParnasCriteria.pdf)
- **Further points** [P]:
  - A symbol table nested inside line storage "was completely invisible to the rest of the system".
  - Decomposition 2 "will prove to be much less efficient" if each function is called as a procedure, so Parnas proposes assembly tools under which module boundaries "may not be clear in the final code".
  - In a translator project, modules such as "register representation, search algorithm, rule interpretation" stayed valid for a compiler and for interpreters. Hence "the order in time in which processing is expected to take place should not be used in making the decomposition into modules".
  - "hierarchical structure and 'clean' decomposition are two desirable but independent properties". The uses relation is out of scope here.
- **Conclusion**: "it is almost always incorrect to begin the decomposition... on the basis of a flowchart. We propose instead that one begins with a list of difficult design decisions or design decisions which are likely to change. Each module is then designed to hide such a decision from the others" [P].
- **Reception** (Parnas's recollection): a referee said "nobody does it that way", Brooks called it "a recipe for disaster", and another reviewer called it "banal" [P*]. [2009 talk abstract](https://www.comp.hkbu.edu.hk/~pgday/2009/talk-sep09.html)

### Inferences
- The unit of decomposition is a design decision (a "secret"), not a type, class or file. Sequencing, calling conventions and character codes count as secrets alongside data structures.
- The criterion depends on a change list. The paper gives no way to build or check that list other than judgment.
- Because a module is a design-time unit, Parnas accepted that module boundaries could vanish in the executable.

### Gaps
- I did not read the 1971 TR or the 1972 SIGCSE course report; DTIC was "Under Maintenance". Parnas's 2009 slides claim the class project gave "1024 possible combinations, 25 tested and made to work" [P*], but I found no original data. [slides](https://www.comp.hkbu.edu.hk/~pgday/2009/10th_PPT/HOSEI%20Making%20Information%20Hiding%20Work%20slides.pdf)

## 2. The module guide, secrets and hierarchical decomposition (Parnas, Clements & Weiss 1984/85; A-7E guide 1981)

### Takeaway
For large systems, PCW add a module guide to information hiding: a tree-structured document stating each module's secrets.
- The **primary secret** is the hidden information given to the designer.
- The **secondary secrets** are the implementation decisions made in hiding it.

A responsibility is written as "the programs that need to be changed if X changes", not as what the code does. I could not get the full PCW paper or the NRL guide. The content below comes from the abstract, a reproduction by co-author Clements, Parnas's 2009 slides and lecture notes.

### Cited Findings
- **Sources**: Parnas, Clements & Weiss, "The Modular Structure of Complex Systems."
  - Conference: *ICSE 7*, 1984, pp. 408–417 ([record](https://experts.mcmaster.ca/scholarly-works/2169057)).
  - Journal: *IEEE TSE* SE-11(3):259–266, Mar 1985, DOI 10.1109/TSE.1985.232209 ([record](https://experts.mcmaster.ca/scholarly-works/2169020)).
  - The abstract covers software that is "inherently complex because of very many arbitrary details" and proposes "a hierarchically structured document, which we call a module guide" [P*, abstract only].
  - Britton & Parnas, "A-7E Software Module Guide," NRL Memorandum Report 4702, 8 Dec 1981, 35 pp. [S]; [DTIC](https://apps.dtic.mil/sti/pdfs/ADA108649.pdf) was offline.
- **Guide rules in Parnas's words** (experience/opinion) [P*]:
  - "Module structures are documented in a Module Guide, which states only the secret of each module."
  - "the structure of the document mirrors that of the system"
  - "Any module may be partitioned (if secrets can change independently)"
  - "Partitioning introduces no new secrets: refines the old ones"
  - "There should be no shared secrets"
  - "Stop partitioning only if a module is easily replaced"
  - "The module guide is the only document read by all"

  [Parnas 2009](https://www.comp.hkbu.edu.hk/~pgday/2009/10th_PPT/HOSEI%20Making%20Information%20Hiding%20Work%20slides.pdf)
- **The two kinds of secret** [S]: "primary secret — hidden information specified to the software designer; secondary secrets — implementation decisions made by the designer when implementing". [Bredereke, Bremen lecture 2002/03](https://www.cs.uni-bremen.de/agbs/lehre/ws0203/scs4/lect-3_2toP232.pdf)
- **Goals**, reproduced in Bass, Clements & Kazman, *Software Architecture in Practice*, 2nd ed. 2003, ch. 3 [S]:
  - "Each module's structure should be simple enough to be understood fully."
  - Change one module's implementation "without knowledge of the implementation of other modules and without affecting the behavior of other modules".
  - "it should be possible to make likely changes without changing any module interfaces; less likely changes may involve interface changes but only for modules that are small and not widely used. Only very unlikely changes should require changes in the interfaces of widely used modules."
  - "If the module interfaces are not revised, it should be possible to run and test any combination of old and new module versions."

  [Bass et al. ch. 3](https://people.ece.ubc.ca/matei/EECE417/BASS/ch03lev1sec3.html) (course-hosted copy)
- **Purpose and form of the guide** [S]:
  - It "defines the responsibilities of each of the modules by stating the design decisions that will be encapsulated by it. Its purpose is to avoid duplication and gaps, to achieve separation of concerns, and, most of all, to help a maintainer find out which modules are affected by a problem report or change request."
  - Each nonleaf node "represents a module composed of the modules represented by its descendants", and the guide says nothing about runtime relationships.
  - Decomposition stops when "each module is small enough to be discarded and begun again if the programmer assigned to it leaves the project".

  [Bass et al.](https://people.ece.ubc.ca/matei/EECE417/BASS/ch03lev1sec3.html)
- **Why a guide is needed** [S]: up to about 25 modules, one can tell which modules a change affects. With "hundreds of modules... information hiding alone does not work here!" Each node should have few enough branches that designers "can argue convincingly that no overlapping responsibilities of submodules, all responsibilities of module are covered". [Bredereke](https://www.cs.uni-bremen.de/agbs/lehre/ws0203/scs4/lect-3_2toP232.pdf)
- **Real A-7E entries** [S]:
  - "The Hardware-Hiding Module includes the procedures that need to be changed if any part of the hardware is replaced by a new unit with a different hardware/software interface but with the same general capabilities... The primary secrets... are the hardware/software interfaces. The secondary secrets... are the data structures and algorithms used to implement the virtual hardware."
  - "The Behavior-Hiding Module includes procedures that need to be changed if there are changes in requirements affecting the required behavior. Those requirements are the primary secret."
  - "The Software Decision Module hides software design decisions that are based on mathematical theorems, physical facts, and programming considerations such as algorithmic efficiency and accuracy... both the secrets and the interfaces are determined by software designers."
  - Application Data Type: secrets are "the data representation used in the variables and the procedures used to implement operations on those variables. Units of measurement... are part of the representation and are hidden."
  - Data Banker: producer and consumers "can be written without knowing when a stored value is updated".

  [Bass et al.](https://people.ece.ubc.ca/matei/EECE417/BASS/ch03lev1sec3.html)
- **Parnas's own notes on the A-7E structure** [P*]:
  - The device-interface rule: "If it affects more than one device, consider it part of the computer".
  - The top level is claimed to be universal: "If the secret is in the software requirements document, it must be (1) or (2). If it is not a requirement, it must be (3). This 'top level' structure appears to be universal" (opinion).

  [Parnas 2009](https://www.comp.hkbu.edu.hk/~pgday/2009/10th_PPT/HOSEI%20Making%20Information%20Hiding%20Work%20slides.pdf)
- **The tree is not access control** [S]:
  - "any program may use any access program of any module in the guide, independent of relative positions in hierarchy". Use is governed by the separate uses hierarchy.
  - "(R)" restricted modules (e.g., hardware diagnostics) should be avoided "because of potentially high costs of change".
  - "(H)" hidden modules have "no use outside this module".
  - Interfaces that may change are wrapped in a higher-level module with an "additional local module guide". [Bredereke](https://www.cs.uni-bremen.de/agbs/lehre/ws0203/scs4/lect-3_2toP232.pdf)
- **Versus object-based design** [S]: modules are "derived by cataloging the changes... perceived to be likely over the system's lifetime", not from "the physical objects inherent in the application". Each team got "a second-level module and all of its descendants". The evidence is an experience report with no controlled comparison. [Bass et al.](https://people.ece.ubc.ca/matei/EECE417/BASS/ch03lev1sec3.html)

### Inferences
- A guide entry is a change-conditional statement ("needs to be changed if…") plus its secrets. It says what is hidden, not what the code does.
- "Partitioning introduces no new secrets" gives a checkable rule: the children's secrets partition the parent's, and no secret appears twice.
- The tree of secrets is independent of who may call whom.

### Gaps
- I did not read the PCW full text or the NRL guide. The wording of the primary/secondary definitions and of the (R)/(H) rules comes from secondary sources. I could not check whether PCW sets numeric size or branching limits.

## 3. Later Parnas: misunderstanding, misapplication, interface and abstraction

### Takeaway
Parnas says repeatedly that the principle is widely endorsed but rarely applied well. People name "how to" steps as secrets, equate the principle with OO languages, let secrets show, and leave the abstraction undocumented. For him an interface is the set of assumptions others may make, not a signature. Hiding without interface documentation is "Brooks' disaster".

### Cited Findings
- **1971 origin**: "The connections between modules are the assumptions which the modules make about each other" [P*]. Liskov quotes this verbatim, citing IFIP 1971: [Liskov 2010](https://web.stanford.edu/class/ee380/Abstracts/110420-turing-10-slides.pdf), [Liskov 2013](https://qconlondon.com/ln2018/london-2013/qconlondon.com/dl/qcon-london-2013/slides/BarbaraLiskov_KeynoteThePowerOfAbstraction.pdf).
  - Colyer's 2016 blog renders the line with "microservices" instead of "modules", which is an editorial change.
  - In a comment on that blog (17 Oct 2016), Parnas said his later papers "talk about the need to design and then document interfaces" [P*]. [Colyer + comment](https://blog.acolyer.org/2016/10/17/information-distribution-aspects-of-design-methodology/)
- **"Software Aging,"** *ICSE 16*, 1994, pp. 279–287, DOI 10.1109/ICSE.1994.296790 [P] (opinion/experience): [PDF](https://www.eecs.yorku.ca/course_archive/2007-08/F/6431/Parnas.pdf).
  - The principle "is known by various names, e.g. 'information hiding', 'abstraction', 'separation of concerns', 'data hiding', or most recently, 'object orientation'."
  - "predictions will be about classes of changes"; "it is important to estimate the probabilities of each type of change".
  - "in spite of its broad acceptance, I do not see much software that is well designed from this point of view".
  - Textbooks "say that one should hide... 'implementation details', but they do not discuss... estimating the probability of change".
  - "Even when told to associate each module with a 'secret'... they use 'secrets' of the form, 'how to ....', and make each module perform some step in the processing".
  - "Programmers tend to confuse design principles with languages... they think that one has applied the techniques, if one has used such a language."
- **"The Secret History of Information Hiding,"** in *Software Pioneers* (Broy & Denert, eds.), Springer 2002, pp. 398–409, DOI 10.1007/978-3-642-59412-0_25 [P*, abstract only]: the idea is "widely accepted in academic circles" but "most industrial software developers do not apply the idea and many consider it unrealistic". [record](https://experts.mcmaster.ca/scholarly-works/1973746)
- **2009 talk** (HKBU, 1 Sep 2009) [P*]:
  - "if you hide some information, you must give people other information to work with"
  - "Information Hiding was the second of two papers. The first was on interface specification. The second without the first would be a disaster."
  - "Secrets show (even in textbook examples). The abstraction is not documented."
  - Why it is hard: the "flowchart instinct", "Planning for change seems like too much planning", "Assumptions often go unnoticed — Major Flaw in my KWIC Index", "Rush to code".
  - Information hiding, ADTs, separation of concerns ("motivation"), OO ("false emphasis on language") and components "are all the same design principle. People focus on the syntax and buzzwords... Ask designers to tell you the secret and they usually cannot. Review reveals distributed secrets and secret-free modules."

  [slides](https://www.comp.hkbu.edu.hk/~pgday/2009/10th_PPT/HOSEI%20Making%20Information%20Hiding%20Work%20slides.pdf)
- **Interface** (definitions, 2009) [P*]:
  - Interfaces are "Often, confused with syntax of invocations or a shared data structure".
  - "B's interface to A is the weakest assumption about B that would allow you to prove that A is correct."
  - Interfaces are asymmetric.
  - If A uses facts about B "not implied by B's specified interface, the actual interface is stronger than the specified interface and A should be considered incorrect (even if it is working)".
  - "B may have an interface with A even if neither invokes the other".
  - "The assumptions in an interface should be unlikely to change". What information is made available or needed is more stable "than assumptions about the representation of such information".
  - Changes "are often only predictable by specialists".

  [slides](https://www.comp.hkbu.edu.hk/~pgday/2009/10th_PPT/HOSEI%20Making%20Information%20Hiding%20Work%20slides.pdf)
- **"Information hiding theorem"** (formal argument with stated empirical premises) [P*]: "If you can prove program A correct knowing only the interface to program B, then if you change B without changing its interface, A need not change." It needs empirical support that "people can know what to hide", that "interfaces can be efficient", and that "we can describe interfaces without revealing secrets".
- **Abstraction, modules, documents** [P*]:
  - "There are no 'Levels of Abstraction'... 'levels' is used properly only if one has defined a relation that is loop free."
  - "Not all programs in an information-hiding work assignment need to be at the same level."
  - A module is a "Task (work-assignments) for developers... Should have a 'secret'... Only module that has to be changed if the hidden decision has to be changed". A component is a "distribution unit", and "A module may include several components".
  - Documents "are not extracted comments (javadoc)".
- **Brooks's reversal**: the 1995 *Mythical Man-Month* 20th Anniversary Edition has the section "Parnas Was Right, and I Was Wrong about Information Hiding" [P, table of contents only]. [sample pages](https://www.ciscopress.com/content/images/9780201835953/samplepages/0201835959.pdf) Parnas's slides wrongly call it the "25th anniversary edition".
- **Practitioners** (opinion) [S]:
  - McConnell, *IEEE Software* 13(2), 1996: his recipe is to list the secrets, mostly "a design decision that you think might change", and assign each "to its own class, subroutine, or other design unit". He notes that "most programmers would rather expose all of a class's private data than write 10 extra lines of code to keep the secrets intact". [McConnell](https://stevemcconnell.com/wp-content/uploads/2017/08/MIAInformationHiding.pdf)
  - Cunningham: programmers "oversimplify these concepts as merely hiding data representations inside classes... A secret... is any aspect that can change as the system evolves". [Cunningham](https://john.cs.olemiss.edu/~hcc/researchMethods/notes/ClassicParnas/ClassicParnasRevisionFinal.pdf)
  - Ousterhout (2018; 2nd ed. 2021) adds "deep modules", "information leakage" and "temporal decomposition" as red flags [S, book notes]. [notes](https://dev.to/danlebrero/book-notes-a-philosophy-of-software-design-cna)

### Inferences
- The misuses fall into six patterns:
  1. A secret means private data only.
  2. A secret means "how to do step X", which is processing decomposition renamed.
  3. The principle is equated with language features.
  4. An interface is taken to be a signature.
  5. Interface documentation is missing.
  6. "Levels" are used without a defined relation.
- Parnas's 1972 "function names and... types of the parameters" is a simplification that he later calls a confusion.
- "All the same design principle" is an opinion, and it blurs Dijkstra's usage (§4).

### Gaps
- I did not read the full text of "Secret History" or the commentaries in *Software Fundamentals: Collected Papers by David L. Parnas* (Hoffman & Weiss, eds., Addison-Wesley 2001; [Goodreads](https://www.goodreads.com/book/show/1416932.Software_Fundamentals)). The 1971 original is also unread, because its CMU link now redirects to the KiltHub home page.

## 4. Dijkstra's separation of concerns (EWD447, 1974) versus information hiding

### Takeaway
Separation of concerns is a discipline of thought: study one aspect (correctness, efficiency, desirability) in isolation while knowing it is only one aspect. It separates aspects of one artifact. Information hiding separates parts of the artifact, deciding which decision each work unit owns. The two meet in Dijkstra's "thin interface" and in his split between specifying a thing and building it.

### Cited Findings
- **Source**: E. W. Dijkstra, EWD447 "On the role of scientific thought," 30 Aug 1974, read in full [P]: [EWD447](https://www.cs.utexas.edu/~EWD/transcriptions/EWD04xx/EWD447.html).
- **Definition**: "one is willing to study in depth an aspect of one's subject matter in isolation for the sake of its own consistency, all the time knowing that one is occupying oneself only with one of the aspects. We know that a program must be correct and we can study it from that viewpoint only; we also know that it should be efficient and we can study its efficiency on another day... It is what I sometimes have called 'the separation of concerns', which, even if not perfectly possible, is yet the only available technique for effective ordering of one's thoughts... it does not mean ignoring the other aspects, it is just doing justice to the fact that from this aspect's point of view, the other is irrelevant" [P].
- **Specification as interface**: "It is the sole purpose of the specifications to act as the interface between the system's users and the system's builders. The task of 'making a thing satisfying our needs' as a single responsibility is split into two parts 'stating the properties of a thing, by virtue of which it would satisfy our needs' and 'making a thing guaranteed to have the stated properties'" [P]. [EWD447](https://www.cs.utexas.edu/~EWD/transcriptions/EWD04xx/EWD447.html)
- **Modules of knowledge**: disciplines need internal "coherence" and externally "a thin interface; the more self-supporting such an intellectual subuniverse, the less detailed the knowledge that its practitioners need about other areas". They are "the natural intellectual modules of our culture", which is "probably the best concise answer" to what "Modularization" means [P].
- **How Parnas maps it**: in 1994, SoC is another name for design for change [P] ([Software Aging](https://www.eecs.yorku.ca/course_archive/2007-08/F/6431/Parnas.pdf)). In 2009, it is "Separation of Concerns (motivation)" [P*].

### Inferences
- **How they differ**:
  - Unit: an aspect of reasoning, versus a design decision.
  - Goal: tractable reasoning, versus changeability and parallel work.
  - Reach: Dijkstra's concerns (correctness, efficiency) cut across every module, so they cannot be module boundaries.
  - Medium: separation of concerns can happen over time ("on another day") and in documents, not only in code structure.
- **Where they meet**: "coherence" plus "thin interface" is a general modularity criterion. The specify/construct split is the contract that Parnas formalizes as interface specification.
- Reading SoC as "one module per concern" is a later interpretation. EWD447 does not say it.

### Gaps
- I did not trace Dijkstra's earlier uses of the phrase. Critiques that one decomposition cannot separate every concern (Tarr et al. 1999, "tyranny of the dominant decomposition"; AOP, Kiczales et al. 1997) were not retrieved; other researchers may cover them.

## 5. Liskov & Zilles (1974): modules, abstract data types and representation hiding (brief)

### Takeaway
Liskov and Zilles turned "a module that hides a data representation" into a language construct. A type is characterized only by its operations, and its representation is visible only inside a CLU cluster. Liskov traces the idea from Parnas 1971 through her 1972 "partitions".

### Cited Findings
- **Source**: Liskov & Zilles, "Programming with Abstract Data Types," SIGPLAN Symposium on Very High Level Languages, *SIGPLAN Notices* 9(4):50–59, Apr 1974, DOI 10.1145/800233.807045. I could not read the original (ACM DL returned 403). [summary](https://users.cs.northwestern.edu/~chrdimo/teaching/eecs396-w19/6.pdf)
- **The paper as quoted on a blog** [S]:
  - "An abstract data type defines a class of abstract objects which is completely characterized by the operations available on those objects".
  - The representation is "accessible only within the cluster".
  - "it is the business of the compiler to map good logical structure into good physical structure".

  [Colyer 2016](https://blog.acolyer.org/2016/10/20/programming-with-abstract-data-types/)
- **Liskov's own slides** [P*]:
  - The line runs Parnas 1971, then "Partitions" (FJCC 1972), then "Connect partitions to data types".
  - The 1974 paper proposed "The operations provide the only way to use the objects" and "Clusters with encapsulation" ([2010](https://web.stanford.edu/class/ee380/Abstracts/110420-turing-10-slides.pdf)).
  - "A using module depends only on the specification", and in 1970 "Procedures were the only type of module" ([2013](https://qconlondon.com/ln2018/london-2013/qconlondon.com/dl/qcon-london-2013/slides/BarbaraLiskov_KeynoteThePowerOfAbstraction.pdf)).

### Inferences
- An ADT is information hiding whose secret is a representation. Parnas's modules hide more: hardware, required behavior, update policies, sequencing. "Depends only on the specification" is the enforceable counterpart of interface-as-assumptions.

### Gaps
- I did not check whether the 1974 paper cites Parnas.

## 6. Concrete, checkable rules for module boundaries derived from the sources

### Takeaway
The sources yield about a dozen rules. Most are review questions that need domain judgment. A few have syntactic proxies that a tool can check.

### Cited Findings
Each rule is followed by its anchor; the quotes are in §1–3.
- **R1 Start from a change list.** "begin with a list of difficult design decisions or design decisions which are likely to change" ([1972](https://www.cse.sc.edu/~mgv/csce590f20/ParnasCriteria.pdf)). Estimate the probability of each class of change ([1994](https://www.eecs.yorku.ca/course_archive/2007-08/F/6431/Parnas.pdf)) [P].
- **R2 One hidden decision per module.** No shared secrets and no secret-free modules ([2009](https://www.comp.hkbu.edu.hk/~pgday/2009/10th_PPT/HOSEI%20Making%20Information%20Hiding%20Work%20slides.pdf)) [P*].
- **R3 A secret is not a step.** "How to…" secrets are a misapplication (1994). Use the A-7E form "need to be changed if…" [S].
- **R4 Ignore execution order** when decomposing (1972).
- **R5 Reveal as little as possible.** Over-specification is "a design error" (1972).
- **R6 Keep data with its access.** A data structure lives with its access and modify procedures; formats, codes, orderings and processing sequence stay hidden (1972).
- **R7 Rely only on the specified interface.** Using unspecified facts makes a client "incorrect (even if it is working)" (2009).
- **R8 Match interface stability to change likelihood.** Old and new module versions should combine freely (PCW via [Bass](https://people.ece.ubc.ca/matei/EECE417/BASS/ch03lev1sec3.html)) [S].
- **R9 Partition only where secrets can change independently.** Children refine the parent with no new secrets, no overlap and nothing left uncovered. Stop when a module is "easily replaced" [P*]/[S].
- **R10 One guide stating only secrets,** read by everyone and kept separate from interface specifications (2009).
- **R11 Keep decomposition, uses and runtime structure apart.** "Levels" need a loop-free relation (1972; 2009).
- **R12 Put shared knowledge in the common module.** "If it affects more than one device, consider it part of the computer" (2009).
- **R13 Ask for the secret.** "Ask designers to tell you the secret and they usually cannot" (2009).

### Inferences
- **Syntactic proxies**:
  - R6: no cross-module mutation of another module's data.
  - R7: imports only through a published surface.
  - R9 and R10: a one-line secret on every node, with parent/child overlap checked in review.
  - R11: layers derived from uses, with the decomposition kept separate.
- R1–R5 and R8 need people with domain knowledge. Parnas notes that changes "are often only predictable by specialists".

### Gaps
- None of these sources validates a metric for a "good secret" or reports a controlled study. The evidence is worked examples and experience (KWIC, the translator, class projects, A-7E). Quantitative re-analyses of KWIC (Sullivan et al. 2001, DSM/option value) and coupling/cohesion metrics are covered by other researchers.

## Relevance to ln-structure

### (a) What the sources support
- **One-line responsibility per module.** This matches a guide entry that "states only the secret of each module" (2009). "Not how it works" matches the 1994 warning against "how to…" secrets.
- **Humans specify, agents implement.** This matches "module = responsibility assignment" (1972) and Dijkstra's split between "stating the properties of a thing" and "making a thing guaranteed to have the stated properties". Parnas 1971 says designers should control which information reaches implementers: "We should not expect a programmer to decide not to use a piece of information" [S, via Colyer]. Surfaces enforce this for agents that can read every file.
- **Imports only via surfaces.** This matches Liskov's "A using module depends only on the specification". Nested modules exposing only their top inner layer resemble PCW's "(H)" hidden submodules with local guides, and the symbol table that was "completely invisible to the rest of the system".
- **Layers computed and carrying no meaning.** This matches "There are no 'Levels of Abstraction'" without a defined loop-free relation, and "hierarchical structure and 'clean' decomposition are... independent".
- **Types-only surfaces and Rust impls kept with the type.** These match 1972 rule 1 and CLU clusters.
- **No import side-effect registration.** This matches "B may have an interface with A even if neither invokes the other": hidden assumptions that appear in no interface.

### (b) What they challenge or contradict
- **A module is a decision, not a folder or class.** Parnas warns that "People focus on the syntax and buzzwords and forget the design principle". Passing `lnt check` does not show that information is hidden.
- **An interface is assumptions, not signatures.** Surfaces check names and types only. Semantic leaks pass: orderings, units, timing, and formats in public attributes. The over-specified KWIC shift order would pass any syntactic check.
- **"Answers or owns" admits step-type lines** (for example "owns input parsing"), which is the 1994 misuse. Parnas's test is about change: which decision is hidden, and which change stays inside.
- **"Exactly one responsibility" versus "one secret".** PCW allow a module to hold secrets that change together, splitting only "if secrets can change independently". Over-splitting produces "distributed secrets".
- **Decomposition and layering are fused.** ln-structure puts modules in layer folders computed from uses. PCW keep the tree of secrets separate from the uses hierarchy, and let any listed module be used regardless of its position in the tree. Same-layer import bans may force splits or merges unrelated to secrets.
- **Missing pieces.** There is no primary/secondary secret distinction, no check that a child's responsibility refines its parent's, and no change list. Without a change list, responsibilities written by humans risk producing secret-free modules.

### (c) Open questions
- Should the responsibility line be phrased as a secret ("hides X; the only module to change if X changes")? Could `lnt` lint step-style lines?
- Should `lnt doc` emit a PCW-style guide (a tree of secrets with (H)/(R) marks) separate from the layer map?
- How can semantic leakage be detected, such as public data attributes, exported format constants or ordering promises?
- Does "people can know what to hide" hold for AI agents? Is enforcement through surfaces enough?
- With agents, rewriting is cheap, so interface change becomes the main cost. Does that favor fewer, deeper modules (Parnas's "easily replaced"; Ousterhout)?
- None of these sources provides controlled evidence. ln-structure could gather its own data, for example the share of change sets confined to one module.
