# Responsibility-Driven Design, CRC Cards, GRASP and Protected Variations: responsibility as the unit of design

## 1. Wirfs-Brock's Responsibility-Driven Design (RDD): definition, discovery, assignment, stereotypes, control styles, design stories

### Source key (full citations used throughout)
- **[WB&W 1989]** Wirfs-Brock, R. & Wilkerson, B. (1989). "Object-Oriented Design: A Responsibility-Driven Approach." *OOPSLA '89 Proceedings* (SIGPLAN Notices 24(10)). DOI 10.1145/74877.74885. Author page: https://wirfs-brock.com/rebecca/papers/oodesign-a-responsibility-driven-approach/. Only the abstract was readable (the ACM PDF returned 403).
- **[DOOS 1990]** Wirfs-Brock, R., Wilkerson, B. & Wiener, L. (1990). *Designing Object-Oriented Software*. Prentice Hall. **Not read directly.** It is available here only through course notes: R. Whitney, SDSU CS535 (2000), https://eli.sdsu.edu/courses/fall00/cs535/notes/analysis/analysis.html, and UTEP CS4311 Lecture 8 "Subsystems" (c. 2018), https://www.cs.utep.edu/isalamah/courses/4311/CS4311-Lecture-8.pdf. Superseded by the 2003 book.
- **[OD 2003]** Wirfs-Brock, R. & McKean, A. (2003; typeset Oct 2002). *Object Design: Roles, Responsibilities, and Collaborations*. Addison-Wesley, ISBN 0-201-37943-0. I read the full text in the publisher's out-of-print PDF: https://ptgmedia.pearsoncmg.com/imprint_downloads/informit/op/9780201379433_objectdesign.pdf. A search listing also shows the authors offering a free copy at https://wirfs-brock.com/rebecca/books/ObjectDesign/. Page numbers below are the book's own. This is the current authoritative statement of RDD.
- **[WB 2014]** Wirfs-Brock, R. (2014). "Object Design Roots and New Directions" (talk slides). https://wirfs-brock.com/rebecca/assets/documents/ObjectDesignRoots.pdf

### Takeaway
RDD defines a responsibility as an obligation to know, do, or decide. Responsibilities are grouped into roles: "a set of related responsibilities". They are stated at a general level, above individual operations, and assigned by heuristics: keep behaviour with information, keep each piece of information in one place, keep each object coherent and within one domain, and don't overlap or over-split. Six role stereotypes and a continuum of control styles (centralized to delegated to dispersed) help characterize objects. A two-paragraph "design story" anchors the search for candidates. All of this is presented as an informal method based on expert experience, not as validated rules.

### Cited Findings
- **Origin and motive.** The 1989 abstract argues that "design practices which take a data-driven approach fail to maximize encapsulation because they focus too quickly on the implementation of objects." It proposes a responsibility-driven alternative that increases encapsulation by deferring implementation decisions. — [WB&W 1989](https://wirfs-brock.com/rebecca/papers/oodesign-a-responsibility-driven-approach/) [primary, abstract only; formal-argument/position paper]
- **Core vocabulary (OD p.3), verbatim:** "An application = a set of interacting objects / An object = an implementation of one or more roles / A role = a set of related responsibilities / A responsibility = an obligation to perform a task or know information / A collaboration = an interaction of objects or roles (or both) / A contract = an agreement outlining the terms of a collaboration." Also: "A role is a slot in the software machinery to be filled with an appropriate object as the program runs" (p.4). — [OD 2003](https://ptgmedia.pearsoncmg.com/imprint_downloads/informit/op/9780201379433_objectdesign.pdf) [primary; definitional]
- **Know / do / decide.** Responsibilities "include three major items: The actions an object performs; The knowledge an object maintains; Major decisions an object makes that affect others" (p.110). "Responsibilities are general statements about what an object knows, does, or decides" (p.112). The 2014 slides list "RDD Principles": "1. Maximize Abstraction — Hide the distinction between data and behavior. Think of object responsibilities for 'knowing', 'doing', and 'deciding'. Focus on what a class should do and how it should be used, first. Then decide on how to implement it. 2. Distribute Behavior … Make objects smart… but not too smart. Delegate responsibility. 3. Preserve Design Flexibility — … Hide implementation details … Implement code so that dependencies between classes are minimized … Create places where your existing design can be extended." — [OD 2003](https://ptgmedia.pearsoncmg.com/imprint_downloads/informit/op/9780201379433_objectdesign.pdf); [WB 2014](https://wirfs-brock.com/rebecca/assets/documents/ObjectDesignRoots.pdf) [primary; expert opinion]
- **Where responsibilities come from (pp.111-112).** The strategy is: "Cover areas that have big impacts. Look for actions to be performed and information that needs to be maintained or created." Use cases are turned into responsibilities in three steps: "Identify things the system does and information it manages. Restate these as responsibilities. Break them down into smaller parts if necessary, and assign them to appropriate objects." A sidebar says: "How to optimally distribute individual responsibilities between objects is often the most difficult problem in object design." — [OD 2003](https://ptgmedia.pearsoncmg.com/imprint_downloads/informit/op/9780201379433_objectdesign.pdf) [primary; expert experience]
- **Public vs private responsibilities (p.126).** Services and information offered to others "are its public responsibilities"; the actions an object takes to support them "are its private responsibilities." — [OD 2003](https://ptgmedia.pearsoncmg.com/imprint_downloads/informit/op/9780201379433_objectdesign.pdf) [primary]
- **Assignment heuristics (pp.132-138), from the bold rule headings:**
  - "Decide how an object will divide or share the work of a large or complex responsibility." The options are to do it all itself, collaborate, or delegate the whole request. "A responsibility that is too complex to be implemented by a single object essentially introduces a new sub design problem."
  - "Make sure an object isn't doing too much." A long list means "Either you are stating its responsibilities in too much detail, or it is taking on too much."
  - "Keep behavior with related information."
  - "Distribute system intelligence." The book adds: "Guard against the tendency to make controllers too intelligent… Our goal isn't to evenly distribute intelligence but to give objects those responsibilities they can handle."
  - "Keep information about one thing in one place." It also warns: "Sometimes we go overboard, factoring out responsibilities into roles that are too small. In that case it is better to pull them back into a single, more responsible object."
  - "Make an object's responsibilities coherent… Everything an object knows or does should contribute to its purpose."
  - "Restrict an object's responsibilities to a single domain."
  - "Avoid taking on nonessential responsibilities." One reviewed design had "a Person object [with] more than 500 methods."
  - "Don't overlap responsibilities."
  
  — [OD 2003](https://ptgmedia.pearsoncmg.com/imprint_downloads/informit/op/9780201379433_objectdesign.pdf) [primary; expert heuristics with worked examples, no empirical test]
- **Quality tests (p.145):** "Does it stick to its purpose? Are its responsibilities clearly stated? Do its responsibilities match its role? Is it of value to other objects in its neighborhood?" From the summary (p.146): "A good test of whether an object is well formed is that its responsibilities form a cohesive unit." — [OD 2003](https://ptgmedia.pearsoncmg.com/imprint_downloads/informit/op/9780201379433_objectdesign.pdf) [primary]
- **Role stereotypes (p.4), verbatim:** "Information holder—knows and provides information; Structurer—maintains relationships between objects and information about those relationships; Service provider—performs work and, in general, offers computing services; Coordinator—reacts to events by delegating tasks to others; Controller—makes decisions and closely directs others' actions; Interfacer—transforms information and requests between distinct parts of our system." They are "purposeful oversimplifications". "An object may fit into more than one stereotype."
  - The book's test for one role versus two: if information "is being used solely to support its service, it assumes two stereotypes but only one role. But if it is perceived as serving two different types of clients for different purposes, it is likely playing two roles" (p.5).
  - The 2014 slides trace stereotypes to "Characterizing Your Objects" (*Smalltalk Report*, Feb 1992). They reword some of them: service provider "performs work on demand"; coordinator "mechanically reacts to events"; interfacer "translates information and requests".
  - The slides recommend using stereotypes to "Think about objects or components needed" and to "Blend roles to make objects more responsible."
  
  — [OD 2003](https://ptgmedia.pearsoncmg.com/imprint_downloads/informit/op/9780201379433_objectdesign.pdf); [WB 2014](https://wirfs-brock.com/rebecca/assets/documents/ObjectDesignRoots.pdf) [primary]
- **Control styles (pp.196-200).**
  - "Deciding on and developing a consistent control style is one of the most important decisions a designer makes."
  - "A control style can be centralized, delegated, or dispersed. But there is a continuum of solutions."
  - Centralized style places "major decision-making responsibilities in only a few objects—those stereotyped as controllers." Its variant is "clustered", where control is "factored among a group of objects whose actions are coordinated."
  - Under delegated style, "Decisions made by controllers will be limited to deciding what should be done… objects with control responsibilities tend to coordinate rather than control every action."
  - Under dispersed style, "it can be hard to locate where a control center is… all decisions have been reduced to very small ones."
  - "Most control designs fit within a band of solutions ranging from centralized (but not overly so) to delegated (but not totally dispersed)."
  - Named pitfalls of centralization: "Control logic can get overly complex"; "Controllers can become dependent on information holders' contents"; "Objects can become coupled indirectly through the actions of their controller"; "The only interesting work is done in the controller."
  - The authors' stated preference is "a delegated control style. We prefer a design in which no one object knows or does too much." They add a caveat: "When you use a framework, it is best to go with the flow and adopt its control style."
  
  — [OD 2003](https://ptgmedia.pearsoncmg.com/imprint_downloads/informit/op/9780201379433_objectdesign.pdf) [primary; expert opinion]
- **Design stories (pp.80-81).** "Write a brief design story. In it, describe what is important about your application." Then identify themes from it. "Write a rough story—two paragraphs or less is ideal. Don't take a lot of time revising and polishing it." The story should "identify the things about your application that you know with certainty, as well as things you don't yet know." — [OD 2003](https://ptgmedia.pearsoncmg.com/imprint_downloads/informit/op/9780201379433_objectdesign.pdf) [primary]
- **Self-characterization.** "Responsibility-Driven Design is an informal method… Responsibilities describe what our software must do to accomplish its purpose" (ch. 2). — [OD 2003](https://ptgmedia.pearsoncmg.com/imprint_downloads/informit/op/9780201379433_objectdesign.pdf) [primary]

### Inferences
- RDD has a granularity hierarchy: responsibility, then role (a coherent set), then object (one or more roles), then neighborhood or subsystem. The "single" thing a well-formed object has is a *purpose* or *role*, not a single responsibility statement. Several short responsibility statements usually make up one role.
- The "two types of clients for different purposes means two roles" test is RDD's closest analogue to client- or actor-based separation criteria (cf. SRP, out of scope here).
- The 2003 book explicitly tempers "distribute system intelligence" ("Our goal isn't to evenly distribute intelligence…"). Secondary sources attribute an "evenly distribute" phrasing to DOOS 1990, so this may be a deliberate revision of the earlier guideline (unverified; see Gaps).

### Gaps
- I could not read the full 1989 paper or DOOS 1990, so the 1990 guideline wording ("Evenly distribute system intelligence", "State responsibilities as generally as possible", etc.) is unverified.
- Wirfs-Brock's IEEE Software design columns (c. 2006-2009) and blog posts were not reviewed because the session's web-search budget ran out.

## 2. Beck & Cunningham's CRC cards: why small cards, and how card size bounds responsibilities

### Takeaway
CRC cards record three things on a 4"×6" card: class name, responsibilities and collaborators. Responsibilities are written as "a handful of short verb phrases, each containing an active verb." The paper does **not** say outright that card size caps the number of responsibilities. Instead it gives a clutter heuristic: when a card gets cluttered, first rephrase more concisely; if the object is still too complex, split it. Wirfs-Brock & McKean later state the space constraint explicitly. The evidence is teaching experience only.

### Cited Findings
- **Citation.** Beck, K. & Cunningham, W. (1989). "A Laboratory for Teaching Object-Oriented Thinking." *OOPSLA '89 Conference Proceedings*, New Orleans, Oct 1-6, 1989; *SIGPLAN Notices* 24(10), pp. 1-6 (page range per Biddle et al. 2002). Full text: http://c2.com/doc/oopsla89/paper.html — [Beck & Cunningham 1989](http://c2.com/doc/oopsla89/paper.html) [primary]
- **Three dimensions.** "We settled on three dimensions which identify the role of an object in a design: class name, responsibilities, and collaborators." "The class name of an object creates a vocabulary for discussing a design." — [Beck & Cunningham 1989](http://c2.com/doc/oopsla89/paper.html) [primary]
- **Responsibilities.** "Responsibilities identify problems to be solved." "A responsibility serves as a handle for discussing potential solutions." "The responsibilities of an object are expressed by a handful of short verb phrases, each containing an active verb. The more that can be expressed by these phrases, the more powerful and concise the design." — [Beck & Cunningham 1989](http://c2.com/doc/oopsla89/paper.html) [primary; expert experience]
- **Collaborators.** "We name as collaborators objects which will send or be sent messages in the course of satisfying responsibilities." "Collaboration is not necessarily a symmetric relation." Spatial layout carries meaning, e.g. "Parts, for example, are often arranged below the whole." — [Beck & Cunningham 1989](http://c2.com/doc/oopsla89/paper.html) [primary]
- **Cards and the clutter/split rule.** "All the information for an object is written on a 4" x 6" index card." The cards "are cheap, portable, readily available, and familiar." "If one of the object becomes too cluttered during this process we copy the information on its card to a new card, searching for more concise and powerful ways of saying what the object does. If it is not possible to shrink the information further, but the object is still too complex, we create a new object to assume some of the responsibilities." — [Beck & Cunningham 1989](http://c2.com/doc/oopsla89/paper.html) [primary]
- **Explicit space constraint (later).** "There isn't enough room on a CRC card to record very many details… Use CRC cards for high-level descriptions." "Space on cards is limited, so use it wisely" (OD pp.128-129). In Wirfs-Brock's variant, CRC means "Candidates, Responsibilities, Collaborators". The unlined side holds the name, a *purpose* statement and stereotypes. The lined side is split "roughly two-thirds for responsibilities and one-third for collaborators" (pp.126-127). — [OD 2003](https://ptgmedia.pearsoncmg.com/imprint_downloads/informit/op/9780201379433_objectdesign.pdf) [primary]
- **Evidence and limits stated by the authors.**
  - "In teaching over a hundred students this course we have encountered no one who was unable to complete the exercise unaided…"
  - "Although we have done no follow-up studies…"
  - "we cannot yet claim a complete methodology."
  - "even weaker programmers, without a deep understanding of objects, could contribute to object designs."
  - When cards were sent to a client, "the recipient was unable to make sense of the cards out of context."
  
  — [Beck & Cunningham 1989](http://c2.com/doc/oopsla89/paper.html) [primary; teaching-experience report, no controlled evaluation]

### Inferences
- The card works as a *physical budget*. Running out of space triggers two steps in a fixed order: rephrase at a higher level of abstraction, then split. A budget enforced by a tool (for example a line-length or count limit) would mirror this mechanism.
- The "out of context" failure suggests that terse responsibility lists depend on shared context, such as a design story or the discussion around the cards.

### Gaps
- No source found that measures the effect of card size on responsibility count. Biddle et al. (2002) tried "smaller cards" but report only preference effects (see §6).

## 3. Larman's GRASP and Protected Variations

### Takeaway
GRASP is a set of nine named heuristics for deciding *which* class gets a responsibility: Information Expert, Creator, Controller, Low Coupling, High Cohesion, Polymorphism, Pure Fabrication, Indirection and Protected Variations. Expert, Creator and Controller propose a placement. Low Coupling and High Cohesion evaluate the alternatives. The other four handle variation. Larman's 2001 column calls PV ≡ OCP ≡ Parnas's information hiding. He scopes it to all "modules", including subsystems and applications, and warns explicitly against speculative over-protection.

### Cited Findings
- **Editions.** Larman, *Applying UML and Patterns*: 2nd ed. Prentice Hall 2001/2002 (ISBN 0-13-092569-1); 3rd ed. Prentice Hall 2004/2005 (ISBN 0-13-148906-2; GRASP in ch. 17-18, per the Pearson TOC [secondary]). The 3rd edition text was **not** accessible (O'Reilly returned 403).
- **2nd-ed. sample chapter (ch. 17, "Design Model: Use-Case Realizations with GRASP Patterns"), verbatim:**
  - "the GRASP patterns as such or by name are not the important thing; they are just a learning aid to help talk about and methodically do fundamental object design."
  - "assignment of responsibilities and the choice of object interactions can be rationally explained and learned."
  - "Information Expert suggests that the object that has the information required to fulfill the responsibility should do it."
  - "Start assigning responsibilities by clearly stating the responsibility." This is phrased as a question, e.g. "Who should be responsible for knowing the sale total?" and "Who is responsible for knowing all the logged sales, and doing the logging?"
  - "When there are alternative design choices, take a closer look at the cohesion and coupling implications… Choose an alternative with good cohesion, coupling, and stability in the presence of likely future changes."
  - "higher coupling in and of itself is not a problem; rather, it is especially coupling to unstable things that is a problem."
  
  — [Larman 2nd ed. ch. 17 sample](https://ptgmedia.pearsoncmg.com/images/0130925691/samplechapter/0130925691.pdf) [primary; pedagogical expert guidance]
- **Controller and layers (2nd-ed. sample).** A facade controller is "satisfactory if there are only a few system operations and the facade controller is not taking on too many responsibilities (in other words, if it is becoming incohesive)." Use-case controllers suit many operations, "to keep each controller class lightweight and focused (in other words, cohesive)." On layers: "The UI layer should not have any domain logic responsibilities. It should only be responsible for user interface tasks." The Creator pattern assigns creation "to a class that aggregates, contains, or records the object to be created." — [Larman 2nd ed. ch. 17 sample](https://ptgmedia.pearsoncmg.com/images/0130925691/samplechapter/0130925691.pdf) [primary]
- **3rd-ed. problem/solution statements, quoted by Wikipedia (Larman 2004).**
  - Information Expert. Problem: "What is a basic principle by which to assign responsibilities to objects?" Solution: "Assign responsibility to the class that has the information needed to fulfill it."
  - Creator: "assign class B the responsibility to create object A if one, or preferably more, of the following apply…"
  - Indirection: "Assign the responsibility to an intermediate object to mediate between other components or services."
  - Low Coupling: "Coupling is a measure of how strongly one element is connected to, has knowledge of, or relies on other elements."
  - High Cohesion: "the responsibilities of a given set of elements are strongly related" (pp.314-315).
  - Polymorphism: "assign responsibility for the behavior—using polymorphic operations—to the types for which the behavior varies."
  - Pure Fabrication: "a class that does not represent a concept in the problem domain."
  - Protected Variations. Problem: "How to design objects, subsystems, and systems so that the variations or instability in these elements [do not have an undesirable impact on other elements]?" Solution: "Identify points of predicted variation or instability; assign responsibilities to create a stable interface around them."
  
  — [Wikipedia: GRASP](https://en.wikipedia.org/wiki/GRASP_(object-oriented_design)) [secondary; Wikipedia flags the article for thin inline citation]
- **PV column: citation.** Larman, C. (2001). "Protected Variation: The Importance of Being Closed." *IEEE Software* 18(3), May/June 2001, pp. 89-91, Design column ed. Martin Fowler. — [Larman 2001](https://martinfowler.com/ieeeSoftware/protectedVariation.pdf) [primary; argument by synthesis plus anecdotes]
- **PV column: the principle and its scope.**
  - The Open–Closed Principle says: "Modules should be both open (for extension and adaptation) and closed (to avoid modification that affect clients). OCP is essentially equivalent to the Protected Variation pattern: Identify points of predicted variation and create a stable interface around them."
  - "OCP is what David Parnas really meant by information hiding."
  - "OCP and PV are two expressions of the same principle—protection against change to the existing code and design at variation and evolution points."
  - "In OCP, the term *module* includes all discrete software elements, including methods, classes, subsystems, applications, and so forth."
  - "PV uses the term *interface* in the broad sense of an access view."
  - PV was first written up by Cockburn (PLoPD 2, 1996) independently of OCP. Larman credits Bob Martin's 1996 C++ Report article for bringing OCP to his attention.
  
  — [Larman 2001](https://martinfowler.com/ieeeSoftware/protectedVariation.pdf) [primary]
- **Information hiding vs data encapsulation.** Parnas's term was widely "misinterpreted… as meaning data encapsulation." Parnas "intended it to mean hide information about the design from other modules, at the points of difficult or likely change." Larman quotes Parnas (1972): "We propose instead that one begins with a list of difficult design decisions or design decisions which are likely to change. Each module is then designed to hide such a decision from the others." — [Larman 2001](https://martinfowler.com/ieeeSoftware/protectedVariation.pdf) [primary]
- **Mechanisms.** "PV is a root principle motivating most of the mechanisms and patterns in programming and design that provide flexibility and protection from variations." The mechanisms listed are: data encapsulation, interfaces, polymorphism, indirection, standards; uniform access; data-driven designs; service lookup; interpreter-driven designs; and reflective or metalevel designs. — [Larman 2001](https://martinfowler.com/ieeeSoftware/protectedVariation.pdf) [primary]
- **Against over-protection.**
  - "You must pick your battles in design, be they at the macro-architectural level or the humble instance field. A good designer can identify the likely points of instability or variation and apply PV to those points but not others. Otherwise, effort is wasted and complexity may arise."
  - "Sometimes, the cost of speculative future proofing… outweighs the cost incurred by a simple, highly coupled 'brittle' design that is reworked as necessary in response to true change pressures."
  - "Novice developers tend toward brittle designs, and intermediates tend toward overly fancy and flexible generalized ones (in ways that never get used). Experts choose with insight."
  - Anecdote: a pager system's scripting interpreter was later removed because "it wasn't needed."
  
  — [Larman 2001](https://martinfowler.com/ieeeSoftware/protectedVariation.pdf) [primary; expert opinion plus two anecdotes]

### Inferences
- GRASP turns RDD's informal heuristics into a decision procedure. You state the responsibility as a "Who is responsible for knowing/doing X?" question, propose a placement (Expert, Creator, Controller), then arbitrate with coupling, cohesion and stability. Information Expert is essentially RDD's "Keep behavior with related information".
- PV is the bridge to module-level thinking: by Larman's definition it applies to "subsystems, applications", and it reinterprets a module's job as *hiding one likely-to-change decision*.

### Gaps
- I did not verify the 3rd ed.'s wording of responsibility types (commonly summarized as "doing"/"knowing") or its contraindications for Information Expert, and its definitions of "variation point" vs "evolution point" are likewise unverified. I also found no sign of a 4th edition (as of Oct 2026, unverified).

## 4. What makes a good responsibility statement (with good and bad examples)

### Takeaway
The sources agree that a good statement says *what* an element knows, does or decides, not *how*. It sits above individual attributes and operations, uses a strong, specific verb, and can be understood with little context. Statements that are too vague ("managing resources") must be decomposed. Statements that are too detailed ("knows first name") must be generalized. Larman adds a question form ("Who should be responsible for knowing X?") that makes the placement decision explicit.

### Cited Findings
- **Level of generality.** "A well-formed responsibility is a high-level statement of what an object knows or does." "Responsibilities are best stated at a level above individual attributes or operations." "Make broad, encompassing general statements of responsibilities. Don't express responsibilities as individual attributes or operations." "The more broadly you state responsibilities, the fewer statements you need" (OD pp.128-129). — [OD 2003](https://ptgmedia.pearsoncmg.com/imprint_downloads/informit/op/9780201379433_objectdesign.pdf) [primary]
- **Good vs bad: too detailed.** Say a Customer "knows its name and preferred ways of being addressed." Do not say "'knows first name,' 'knows last name,' 'knows nickname,' 'knows title,' … far too much detail." "There may be 10 ways to ask for tax calculations that are covered by the statement 'Calculate all taxes based on locale.'" (p.129). — [OD 2003](https://ptgmedia.pearsoncmg.com/imprint_downloads/informit/op/9780201379433_objectdesign.pdf) [primary]
- **Good vs bad: too vague or too big.** "What object should be responsible for 'interacting with the user' or 'performing business functions' or 'managing resources' or 'doing the work'? If a responsibility seems too big or too vague, break it into smaller, more specific ones… Treat the 'big responsibility' as a problem statement" (p.138). — [OD 2003](https://ptgmedia.pearsoncmg.com/imprint_downloads/informit/op/9780201379433_objectdesign.pdf) [primary]
- **Verbs (p.131).** "Use strong descriptions… Behind a wall of vagueness can lie details that should not be ignored."
  - Table 4-1, strong verbs: "remove, merge, calculate, credit, register, debit, activate".
  - Table 4-1, weak verbs: "organize, record, find, process, maintain, list, accept".
  - The book adapts this advice from Kulak & Guiney's guidance on use-case names.
  - Exception: "A weak-sounding phrase may have specific meaning in a certain context". In real estate, "Listing a property" has a precise meaning (p.132).
  
  — [OD 2003](https://ptgmedia.pearsoncmg.com/imprint_downloads/informit/op/9780201379433_objectdesign.pdf) [primary; expert opinion]
- **Context-independence and abstraction level.** "Your statements of responsibilities should be understandable with only a small amount of context setting." "The more general a concept, the more general its responsibilities. The more specific a concept, the more specific its duties" (pp.129-131). — [OD 2003](https://ptgmedia.pearsoncmg.com/imprint_downloads/informit/op/9780201379433_objectdesign.pdf) [primary]
- **Exemplar statement sets.**
  - POSA's MVC is broad and role-level. Model: "Registers dependent views and controllers"; "Notifies dependent components about changes in state."
  - DOOS 1990 is "terse, and more specific". Document: "Access and modify elements", "Copy portions of itself", "Knows its views". DisplayFrame: "Displays itself", "Knows its bounding box."
  - The EmailAddress card: "Knows alias of receiver", "Knows signature of sender", "Knows SMTP address info", "Sends a message."
  - A teakettle restated "as general responsibilities": "Pour contents without spilling or splashing; Hold water that can be heated until boiling; Notify when water boils."
  
  — [OD 2003](https://ptgmedia.pearsoncmg.com/imprint_downloads/informit/op/9780201379433_objectdesign.pdf) [primary]
- **Purpose statements (a one- or two-sentence characterization on the card's front).**
  - Pattern: "An object is a type of thing that does and knows certain things. Briefly, say what those things are. Then mention one or more interesting facts about the object…"
  - For service providers, controllers and coordinators: "some kind of thing that does some kind of work."
  - Example: "A RazzmaFrazzer is a converter that accurately and speedily translates Razzma objects into Frazz objects."
  - "Describe both what a candidate is and what it is not. Relate it to what's familiar" (pp.94-95).
  - A related naming rule: "Give names that will be meaningful to those who will be using the candidate, not those who will be implementing it" (p.92). AccountingService "isn't specific" (p.92).
  
  — [OD 2003](https://ptgmedia.pearsoncmg.com/imprint_downloads/informit/op/9780201379433_objectdesign.pdf) [primary]
- **Phrasing in CRC.** Beck & Cunningham ask for "short verb phrases, each containing an active verb" ([Beck & Cunningham 1989](http://c2.com/doc/oopsla89/paper.html) [primary]). Biddle et al. teach that responsibilities are "'things to do, and things to know'" and "should outline what, rather than how… [leading] to the separation of the interface from the implementation details." They also note that "responsibility denotes both duty and power… It permits some freedom in exactly how the obligations are accomplished." — [Biddle, Noble & Tempero 2002](https://people.cs.pitt.edu/~chang/231/5spec/CRCcard/Biddle-Reflection.pdf) [primary; teaching experience]
- **Question form.** "Start assigning responsibilities by clearly stating the responsibility: Who should be responsible for knowing the sale total?" — [Larman 2nd ed. ch. 17](https://ptgmedia.pearsoncmg.com/images/0130925691/samplechapter/0130925691.pdf) [primary]

### Inferences
- Bad statements tend to fail in one of four ways: a weak or generic verb (process, manage, handle, maintain), too broad a scope (the "world peace" problem), implementation detail (attribute or operation lists), or reliance on unstated context.
- The sources do **not** demand a single verb per element. Statements are short and verb-led, but an element normally carries "a handful" of them.

### Gaps
- No source gives a formal grammar or length limit for responsibility statements. All guidance is stylistic.

## 5. Transfer from objects to modules, subsystems and components

### Takeaway
The transfer to larger units is explicit in this literature, not merely inferred.
- DOOS (1990), via secondary notes, treats a subsystem as a responsibility-bearing unit that differs from a class only "in scale". Its contracts are delegated to inner classes.
- *Object Design* (2003) gives "neighborhoods" and subsystems "collective responsibilities", "coherent" roles and a facade.
- Larman's PV/OCP covers "subsystems, applications".
- No dedicated, separately named component-level RDD method was found.

### Cited Findings
- **DOOS 1990 on subsystems, as summarized in course notes:**
  - "Subsystems are groups of classes, or groups of classes and other subsystems"; "There is no conceptual difference between the responsibilities of a class and a subsystem of classes"; "The difference between a class and subsystem of classes is a matter of scale."
  - "There should be as little communication between different subsystems as possible"; "All objects which have strong coupling should be placed in the same subsystem"; "Too many contracts in one subsystem can be a sign that the subsystem has too much intelligence."
  - Contracts are a "Cohesive set of responsibilities that a client can depend on". The notes advise to "Group responsibilities used by the same clients" and to "Minimize the number of contracts."
  
  — [Whitney, SDSU CS535 notes on DOOS ch. 6-8](https://eli.sdsu.edu/courses/fall00/cs535/notes/analysis/analysis.html) [secondary]
- **DOOS 1990 subsystem cards and guidelines.**
  - Subsystems are "Groups of classes that collaborate among themselves to support a set of contracts". They "should provide a good abstraction" and "a clearly defined interface, called subsystem contracts". They "are not 'just a bunch of classes.'"
  - A subsystem card records a purpose and its contracts. "For each contract, identify the class or subsystem to which the contract is delegated." Example: "Drawing Subsystem … Description: Responsible for displaying and maintaining the contents of the drawing."
  - Guidelines: "Minimize the number of collaborations a class has with other classes or subsystems"; "Minimize number of classes and subsystems to which a subsystem delegates"; "Minimize number of contracts supported by a class or subsystem"; "centralize communications into and out of the subsystem."
  - Subsystems can be found bottom-up ("Partition the classes based on patterns of collaborations") or top-down.
  
  — [UTEP CS4311 Lecture 8, based on DOOS ch. 7](https://www.cs.utep.edu/isalamah/courses/4311/CS4311-Lecture-8.pdf) [secondary]
- **Object Design 2003 on neighborhoods and subsystems:**
  - "If every part is connected, then it is hard to limit the effects of change. So it is better to isolate parts—to identify subsystems of objects—and establish patterns of communication between them. Each subpart should have a coherent role; obligations shouldn't spill across different areas" (p.145).
  - "object neighborhoods collectively take on larger, related responsibilities… They, too, should be coherent wholes" (p.145).
  - "As we organize objects into neighborhoods with collective responsibilities… We also decide how objects outside a neighborhood will interact with services that the neighborhood offers" (ch. 5).
  - On too many outside connections: "Exposing all of a neighborhood's objects defeats this purpose… A facade is an internal interfacer with a restricted set of responsibilities." Its responsibilities are "Knowing which objects inside the neighborhood are responsible for handling any external request; Delegating requests to appropriate objects" (ch. 5).
  - "In a large system, it is useful to … identify the guarantees, obligations, and responsibilities of each component" (ch. 8, trust regions).
  - "A reusable role is best specified as an interface that can be implemented by one or more classes" (p.80).
  
  — [OD 2003](https://ptgmedia.pearsoncmg.com/imprint_downloads/informit/op/9780201379433_objectdesign.pdf) [primary; expert opinion]
- **Layer-like "domains" (via Page-Jones 1999).**
  - "objects that live in lower domains shouldn't have responsibilities that tie them to objects in a higher domain. The more you tie objects in a lower domain to a higher one, the harder it is to reuse them in different contexts." The domains run Application, Business, Architectural, Foundation (subdivided Fundamental, Structural, Semantic).
  - Test: "Can one object be built without any knowledge of the other? If so, these two objects aren't likely to be in the same domain."
  - Example: Measurements may "know their temperature" but "don't give Temperatures the ability to convert to higher life forms" (pp.135-136).
  
  — [OD 2003](https://ptgmedia.pearsoncmg.com/imprint_downloads/informit/op/9780201379433_objectdesign.pdf) [primary, citing Page-Jones]
- **Components in Wirfs-Brock's later material.** The 2014 slides apply stereotypes to "objects or components". A telco integration example states that "Components at the edges take on extra responsibility to scrub requests from untrusted sources." — [WB 2014](https://wirfs-brock.com/rebecca/assets/documents/ObjectDesignRoots.pdf) [primary; experience]
- **Larman on scope.** The OCP "module includes … classes, subsystems, applications"; PV's problem is stated for "objects, subsystems, and systems"; and PV applies "from the largest architectural concerns to the smallest coding decision." — [Larman 2001](https://martinfowler.com/ieeeSoftware/protectedVariation.pdf) [primary]; [Wikipedia: GRASP](https://en.wikipedia.org/wiki/GRASP_(object-oriented_design)) [secondary]

### Inferences
- The DOOS subsystem card, with a one-line "Responsible for…" description plus a list of contracts each delegated to an inner element, is the closest historical precedent for a module-level responsibility line backed by a published surface.
- RDD's facade differs from a generated re-export surface. It is a *designed* object with its own (restricted) responsibilities, chosen to minimize the externally visible set.

### Gaps
- I found no empirical study of responsibility-based decomposition at package or component level. Component methods that build on responsibilities, such as Catalysis (1998) and *UML Components* (2000), were not reviewed.

## 6. Critiques, limitations and empirical evidence

### Takeaway
The evidence base is thin and almost entirely experiential: teaching reports, worked examples and one industrial comparison known only second-hand. The strongest empirical study found concerns the *noun-based concept identification* step that precedes responsibility assignment, and it is negative. The authors themselves name several hazards: over-splitting, glue objects, framework-imposed control styles, and speculative PV.

### Cited Findings
- **Sharble & Cohen.** Wirfs-Brock cites "The Object-Oriented Brewery: A Comparison of Two Object-Oriented Methods," R. Sharble & S. Cohen, *Boeing Technical Report BCS-G4059*, 1992, together with her own "How Designs Differ" (*Smalltalk Report* 1(4)). Her slides contrast the data-driven approach (centralized control, controllers, inherited attributes, "many low-level messages", "lots of simplistic information holders") with the responsibility-driven one (delegated control, coordinators, inherited behavior, "fewer, higher-level messages", "a few smart objects that blend role stereotypes"). — [WB 2014](https://wirfs-brock.com/rebecca/assets/documents/ObjectDesignRoots.pdf) [primary for her characterization; the study itself is unread. It is a single-system comparison reported by an interested party. A journal version is often cited as ACM SIGSOFT SEN 1993, which I could not verify.]
- **Biddle, Noble & Tempero (2002).** "Reflections on CRC Cards and OO Design," *TOOLS Pacific 2002*, CRPIT vol. 10, pp. 201-205.
  - Setting: a ~150-student university course run twice, plus six industry courses of ~15 people each, "approximately 400 participants, working in approximately 100 teams", observed over 18 months.
  - Strengths: cards support open discussion of static structure, carry "built-in heuristics that guide design", and support roleplay.
  - Weaknesses: teams preferred notebooks and whiteboards, even after trying "smaller cards"; learners confused classes with objects and system objects with real-world actors.
  - Roleplay risk: "a team may decide a roleplay is successful, when in fact it may well be incomplete or even impossible."
  - Conclusion: CRC remains effective, given compensating strategies.
  
  — [Biddle, Noble & Tempero 2002](https://people.cs.pitt.edu/~chang/231/5spec/CRCcard/Biddle-Reflection.pdf) [primary; observational experience report, uncontrolled]
- **Svetinović, Berry & Godfrey (2005).** "Concept identification in object-oriented domain analysis: why some students just don't get it," *RE'05*, pp. 189-198. They evaluated work by "over 740 students" on "over 135 software requirements specifications" (University of Waterloo, over four years), concluding that "object orientation is poorly suited to domain analysis." The difficulties were independent of system size and of student ability. — [SWAG Waterloo abstract page](https://swag.uwaterloo.ca/publications/concept-identification-in-object-oriented-domain-analysis-why-some-students-just-don-t-get-it.html) [primary abstract, read through a summarizing fetch tool; artifact-analysis study]
- **Mayes (1992).** An analytic University of Hertfordshire report (CSTR 149). Its abstract notes that "The responsibility driven method can lead to the identification of classes which provide one service only and act on data provided by or stored in other objects of another class." — [Mayes 1992](https://uhra.herts.ac.uk/handle/2299/4682) [primary abstract; analytic, neutral in tone]
- **The authors' own cautions.**
  - Over-splitting: "Sometimes we go overboard, factoring out responsibilities into roles that are too small" (OD p.134).
  - Glue objects: "Too many objects with responsibilities to 'glue' others together can also make a design brittle and hard to understand" (p.137).
  - Frameworks dictate control style (ch. 6).
  - Beck & Cunningham: "no follow-up studies".
  - Larman: GRASP names are "just a learning aid"; speculative PV is a typical intermediate-level error.
  
  — [OD 2003](https://ptgmedia.pearsoncmg.com/imprint_downloads/informit/op/9780201379433_objectdesign.pdf); [Beck & Cunningham 1989](http://c2.com/doc/oopsla89/paper.html); [Larman 2001](https://martinfowler.com/ieeeSoftware/protectedVariation.pdf) [primary]

### Inferences
- The guidance on *how to state and assign* responsibilities rests on expert consensus across independent authors (Beck/Cunningham, Wirfs-Brock, Larman, Biddle et al.), not on controlled evidence.
- Svetinović et al. weaken the classic route of finding nouns first and then assigning responsibilities. RDD's own emphasis on roles and behaviour first is partly a response to that weakness, but it is not itself validated.

### Gaps
- No controlled experiment on RDD, CRC or GRASP effectiveness was found. GRASP-specific empirical studies could not be searched (search budget exhausted).
- The Sharble & Cohen report could not be read.

## Relevance to ln-structure

### (a) What the sources support
- **One responsibility line, saying "what, not how".** This matches WB&W 1989 (defer implementation), "Focus on what a class should do… first. Then decide on how to implement it" (WB 2014), and Biddle et al.'s "what, rather than how". It also fits the split between humans who specify and agents who implement: RDD makes responsibility assignment precede implementation.
- **A module-level responsibility is legitimate.** DOOS treats subsystems as differing from classes only "in scale", and its subsystem card carries a one-line "Responsible for…" description. *Object Design* asks neighborhoods and subsystems to be "coherent wholes" whose "obligations shouldn't spill across different areas".
- **Strictly downward dependencies, no cycles.** Page-Jones's rule that lower domains must not be tied to higher ones (§5) supports this. So does Biddle et al.'s rule that only the *user* lists the helper as collaborator, so the helper "can remain independent" ([Biddle et al. 2002](https://people.cs.pitt.edu/~chang/231/5spec/CRCcard/Biddle-Reflection.pdf)).
- **Imports only through surfaces; a nested module exposes only its top inner layer.** RDD's facade rationale and DOOS's advice to centralize communication into and out of a subsystem and minimize contracts (§5) support this.
- **Dependency inversion as a last resort.** Larman's "pick your battles" supports applying PV only at real variation points, and his warning against "overly fancy and flexible generalized" designs supports treating speculative abstraction as a mistake.
- **Rust impl blocks live with their type or trait.** This matches "Keep behavior with related information" and Information Expert.
- **Modules publish only types.** RDD's unit of responsibility is the object or role, and "a reusable role is best specified as an interface".

### (b) What they challenge or contradict
- **Terminology mismatch.** In RDD a *responsibility* is one of several short verb phrases. The unit that is "single" is the *role* ("a set of related responsibilities") or the *purpose*. ln-structure's "exactly one responsibility" corresponds to RDD's purpose or role level. Reports should not equate the two.
- **"Answers or owns" covers mainly knowing.** It fits information holders and structurers ("knows and provides information", "maintains relationships"). It under-describes RDD's *doing* (service provider) and *deciding* (controller, coordinator) responsibilities, which RDD treats as first-class.
- **Semantic vs computed layers.** RDD's layering analogue (Page-Jones domains) is *semantic* (application/business/architectural/foundation). ln-structure's computed, meaning-free layers drop that semantic check.
- **Control style under strict layering.** No same-layer imports and the DI-as-last-resort rule leave centralized or clustered control at the top with delegation downward. Peer collaboration (e.g. a model notifying views) and dispersed control require inversion. This may conflict with the authors' stated preference for delegated control. RDD also says to "go with the flow" of a framework's style.
- **Risk of over-splitting.** One class per file plus one responsibility per module could push designs toward the data-driven profile Wirfs-Brock criticizes ("lots of simplistic information holders"), or toward "roles that are too small" and brittle "glue" objects. Mayes notes that RDD itself can yield single-service classes acting on other classes' data. Forcing free functions into static methods may create exactly such classes.
- **Context dependence.** CRC lines failed "out of context" (Beck & Cunningham), and RDD pairs responsibilities with purpose statements and design stories. A bare one-liner may be too thin for an agent without such context.

### (c) Open questions
- Should the module line be modeled on RDD's *purpose statement* ("An X is a … that …"), on a terse *responsibility* phrase, or on Larman's question form ("Who knows/decides X?")?
- Should the tool lint for weak or vague verbs (process, manage, handle, maintain), which RDD flags, while allowing domain-specific exceptions?
- Is there an analogue of the card budget, such as a line-length limit that triggers "rephrase, then split"?
- How should modules whose real job is *deciding* or *coordinating* be phrased within "answers or owns"?
- How would one detect over-splitting (roles "too small") as well as overload, both of which RDD warns about?
- No controlled evidence exists that responsibility-first decomposition improves maintainability. Any claim of benefit for ln-structure would need its own evaluation.
