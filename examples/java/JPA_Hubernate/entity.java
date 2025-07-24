// Post.java
@Entity
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Post {

    @Id
    @GeneratedValue
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    private Blog blog;

    @ManyToOne(fetch = FetchType.LAZY)
    private Author author;

    private String title;
    private String content;

    private LocalDateTime postedAt;

    @OneToMany(mappedBy = "post")
    private List<PostSection> postSections = new ArrayList<>();
}

// PostSection.java
@Entity
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class PostSection {

    @Id
    @GeneratedValue
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    private Blog blog;

    @ManyToOne(fetch = FetchType.LAZY)
    private Author author;

    @ManyToOne(fetch = FetchType.LAZY)
    private Post post;

    private String content;

    @Column(unique = true)
    private String sectionCode;

    @Enumerated(EnumType.STRING)
    private SectionStatus sectionStatus;

    private boolean permitComment;
}